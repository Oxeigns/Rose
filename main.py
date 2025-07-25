"""Main entrypoint for the Rose Telegram bot.

Set ``DEPLOY_MODE=worker`` to run using long polling (Render background worker).
Set ``DEPLOY_MODE=webhook`` together with ``WEBHOOK_URL`` to run as a web
service processing updates via FastAPI.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client, idle, filters
from pyrogram.handlers import (
    MessageHandler,
    CallbackQueryHandler,
    RawUpdateHandler,
)

from plugins import register_all

from db import init_db

# -------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "debug.log", encoding="utf-8"),
    ],
)

error_handler = logging.FileHandler(LOG_DIR / "error.log", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(error_handler)

LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.DEBUG)

# Log uncaught asyncio exceptions
def _loop_exception_handler(loop, context) -> None:
    msg = context.get("message")
    exc = context.get("exception")
    if exc:
        LOGGER.exception("Unhandled exception: %s", exc)
    elif msg:
        LOGGER.error("Unhandled exception: %s", msg)

asyncio.get_event_loop().set_exception_handler(_loop_exception_handler)

# -------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Deployment mode: "worker" for long polling or "webhook" for FastAPI
DEPLOY_MODE = os.getenv("DEPLOY_MODE", "worker").lower()
USE_WEBHOOK = DEPLOY_MODE == "webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))

if USE_WEBHOOK and not WEBHOOK_URL:
    LOGGER.error("DEPLOY_MODE=webhook but WEBHOOK_URL is not set")
    raise SystemExit(1)

if not all([API_ID, API_HASH, BOT_TOKEN]):
    LOGGER.error("❌ API_ID, API_HASH, and BOT_TOKEN must be provided.")
    raise SystemExit(1)

API_ID = int(API_ID)

# -------------------------------------------------------------
# Bot Client with plugin support
# -------------------------------------------------------------
# IMPORTANT: Handlers are registered manually via the plugins package.

COMMAND_PREFIXES = ["/", "!", "."]

class RoseClient(Client):
    """Client subclass that logs handler registration and errors."""

    def add_handler(self, handler, group=0):
        name = getattr(handler.callback, "__name__", str(handler.callback))
        LOGGER.info("🔗 Registering handler %s (group=%s)", name, group)

        async def wrapped(client, *args, **kwargs):
            try:
                await handler.callback(client, *args, **kwargs)
            except Exception as e:  # pragma: no cover - runtime logging
                LOGGER.exception("❌ Error in handler %s: %s", name, e)
                raise

        handler.callback = wrapped
        return super().add_handler(handler, group)


app = RoseClient(
    "rose_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Patch filters.command globally for common prefixes
_orig_command = filters.command

def _command_patch(commands, prefixes=None, *args, **kwargs):
    prefixes = prefixes or COMMAND_PREFIXES
    return _orig_command(commands, prefixes=prefixes, *args, **kwargs)

filters.command = _command_patch


# -------------------------------------------------------------
# Debug handlers to trace all incoming updates
# -------------------------------------------------------------
async def _debug_message(client: Client, message):
    LOGGER.debug(
        "[MSG] %s (%s) in %s (%s): %s",
        message.from_user.first_name if message.from_user else "N/A",
        message.from_user.id if message.from_user else "N/A",
        message.chat.title if message.chat else "PM",
        message.chat.id if message.chat else "N/A",
        (message.text or message.caption or "").replace("\n", " "),
    )


async def _debug_query(client: Client, query):
    LOGGER.debug(
        "[CB] %s (%s) in %s (%s): %s",
        query.from_user.first_name if query.from_user else "N/A",
        query.from_user.id if query.from_user else "N/A",
        query.message.chat.title if query.message else "PM",
        query.message.chat.id if query.message else "N/A",
        query.data,
    )


async def _debug_raw(client: Client, update, users, chats):
    LOGGER.debug("[RAW] %s", update)


app.add_handler(MessageHandler(_debug_message, filters.all), group=-1)
app.add_handler(CallbackQueryHandler(_debug_query), group=-1)
app.add_handler(RawUpdateHandler(_debug_raw), group=-1)


@app.on_message(filters.all)
async def log_message(client: Client, message) -> None:
    """Log every incoming message."""
    LOGGER.info(
        "[LOG] %s (%s) in %s (%s): %s",
        message.from_user.first_name if message.from_user else "N/A",
        message.from_user.id if message.from_user else "N/A",
        message.chat.title if message.chat else "PM",
        message.chat.id if message.chat else "N/A",
        (message.text or message.caption or "").replace("\n", " "),
    )


# -------------------------------------------------------------
# Delete webhook to enable polling
# -------------------------------------------------------------
async def _delete_webhook(client: Client) -> None:
    """Remove any webhook (if set) to enable polling mode."""
    LOGGER.debug("🌐 Deleting existing webhook (if any)...")
    try:
        result = await client.delete_webhook(drop_pending_updates=True)
        if result:
            LOGGER.info("✅ Webhook deleted successfully.")
        else:
            LOGGER.warning("⚠️ Failed to delete webhook via Bot API")
    except Exception as e:
        LOGGER.warning("⚠️ Exception while deleting webhook: %s", e)


async def _set_webhook(client: Client) -> None:
    """Set webhook for Bot API mode."""
    if not WEBHOOK_URL:
        LOGGER.error("WEBHOOK_URL not provided")
        return
    LOGGER.debug("🌐 Setting webhook to %s", WEBHOOK_URL)
    try:
        result = await client.set_webhook(WEBHOOK_URL)
        if result:
            LOGGER.info("✅ Webhook set successfully.")
        else:
            LOGGER.warning("⚠️ Failed to set webhook via Bot API")
    except Exception as e:
        LOGGER.warning("⚠️ Exception while setting webhook: %s", e)


# -------------------------------------------------------------
# Bot lifecycle
# -------------------------------------------------------------
async def main() -> None:
    LOGGER.info("🚀 Starting Rose bot...")

    try:
        plugin_count = register_all(app)
    except Exception as e:
        LOGGER.exception("❌ Failed loading plugins: %s", e)
        return

    async with app:
        if USE_WEBHOOK:
            LOGGER.info("🌐 Setting webhook...")
            await _set_webhook(app)
        else:
            LOGGER.info("🌐 Deleting existing webhook (if any)...")
            await _delete_webhook(app)

        LOGGER.debug("📚 Initializing database...")
        await init_db()
        LOGGER.info("✅ Database ready")

        handler_count = sum(len(g) for g in app.dispatcher.groups.values())
        LOGGER.info(
            "🔌 Loaded %s plugin(s) with %s handler(s) across %s group(s)",
            plugin_count,
            handler_count,
            len(app.dispatcher.groups),
        )
        LOGGER.info(
            "🤖 Bot started in %s mode", "Webhook" if USE_WEBHOOK else "Polling"
        )
        LOGGER.info("✅ Bot is ready to receive updates")

        await idle()

    LOGGER.info("✅ Bot stopped cleanly.")


# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        if DEPLOY_MODE == "webhook":
            from web import setup, run
            import threading

            setup(app)
            threading.Thread(target=run, daemon=True).start()
            asyncio.run(main())
        else:
            asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("🔌 Interrupted. Exiting...")
