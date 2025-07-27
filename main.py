"""Main entrypoint for the Rose Telegram bot."""

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler, RawUpdateHandler

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

# Asyncio loop exception handling
def _loop_exception_handler(loop, context) -> None:
    exc = context.get("exception")
    msg = context.get("message")
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
DEPLOY_MODE = os.getenv("DEPLOY_MODE", "polling").lower()
USE_WEBHOOK = DEPLOY_MODE == "webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if USE_WEBHOOK and not WEBHOOK_URL:
    LOGGER.error("DEPLOY_MODE=webhook but WEBHOOK_URL is not set")
    raise SystemExit(1)

if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("❌ API_ID, API_HASH, and BOT_TOKEN must be provided.", file=sys.stderr)
    raise SystemExit(1)

API_ID = int(API_ID)

COMMAND_PREFIXES = ["/", "!", "."]

# -------------------------------------------------------------
# Custom Client
# -------------------------------------------------------------
class RoseClient(Client):
    """Client subclass that logs handler registration and prevents recursion."""

    def add_handler(self, handler, group=0):
        name = getattr(handler.callback, "__name__", str(handler.callback))
        LOGGER.info("🔗 Registering handler %s (group=%s)", name, group)

        # Skip wrapping for debug handlers to avoid recursion
        if name in {"log_all_messages", "_debug_query", "_debug_raw"}:
            return super().add_handler(handler, group)

        orig_callback = handler.callback

        async def wrapped(client, *args, **kwargs):
            try:
                await orig_callback(client, *args, **kwargs)
            except Exception:
                LOGGER.exception(f"❌ Exception in handler {name}")

        handler.callback = wrapped
        return super().add_handler(handler, group)


app = RoseClient(
    "rose_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Patch filters.command globally
_orig_command = filters.command
def _command_patch(commands, prefixes=None, *args, **kwargs):
    prefixes = prefixes or COMMAND_PREFIXES
    return _orig_command(commands, prefixes=prefixes, *args, **kwargs)
filters.command = _command_patch

# -------------------------------------------------------------
# Debug Handlers
# -------------------------------------------------------------
async def _debug_query(client: Client, query):
    user = query.from_user.id if query.from_user else "N/A"
    chat = query.message.chat.id if query.message else "PM"
    LOGGER.debug(f"[CB] {user} in {chat}: {query.data}")

async def _debug_message(client: Client, message):
    """Lightweight debug logger for incoming messages."""
    if message.from_user and message.from_user.is_self:
        return
    user = message.from_user.id if message.from_user else "N/A"
    chat = message.chat.id if message.chat else "PM"
    text = message.text or message.caption or ""
    clean_text = text.replace("\n", " ")
    LOGGER.debug(f"[MSG] {user} in {chat}: {clean_text}")

async def _debug_raw(client: Client, update, users, chats):
    LOGGER.debug(f"[RAW] {update}")

app.add_handler(CallbackQueryHandler(_debug_query), group=-1)
app.add_handler(RawUpdateHandler(_debug_raw), group=-1)
app.add_handler(MessageHandler(_debug_message, filters.all), group=-1)

# -------------------------------------------------------------
# Safe log_all_messages
# -------------------------------------------------------------
@app.on_message(filters.all)
async def log_all_messages(client: Client, message):
    """Safely log messages without deep object introspection."""
    if message.from_user and message.from_user.is_self:
        return
    user = message.from_user.id if message.from_user else "unknown"
    text = message.text or message.caption or "<no text>"
    LOGGER.debug(f"Message from {user}: {text}")

# -------------------------------------------------------------
# Webhook utils
# -------------------------------------------------------------
async def _delete_webhook(client: Client) -> None:
    LOGGER.debug("🌐 Deleting existing webhook (if any)...")
    if hasattr(client, "delete_webhook"):
        await client.delete_webhook(drop_pending_updates=True)

async def _set_webhook(client: Client) -> None:
    if not WEBHOOK_URL:
        return
    LOGGER.debug("🌐 Setting webhook to %s", WEBHOOK_URL)
    await client.set_webhook(WEBHOOK_URL)

# -------------------------------------------------------------
# Main
# -------------------------------------------------------------
async def _startup() -> None:
    plugin_count = register_all(app)
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

async def _run_polling() -> None:
    LOGGER.info("🚀 Starting Rose bot in polling mode...")
    async with app:
        await _delete_webhook(app)
        await _startup()
        LOGGER.info("✅ Bot is ready to receive updates")
        await idle()
    LOGGER.info("✅ Bot stopped cleanly.")

async def _run_webhook() -> None:
    LOGGER.info("🚀 Starting Rose bot in webhook mode...")
    from web import setup, web_app
    import uvicorn

    setup(app)
    await app.start()
    await _set_webhook(app)
    await _startup()
    LOGGER.info("✅ Bot is ready to receive updates")

    port = int(os.getenv("PORT", "10000"))
    config = uvicorn.Config(web_app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())
    try:
        await idle()
    finally:
        server.should_exit = True
        try:
            await server_task
        except asyncio.CancelledError:
            LOGGER.info("Server task cancelled during shutdown.")
        await app.stop()
    LOGGER.info("✅ Bot stopped cleanly.")

if __name__ == "__main__":
    try:
        if USE_WEBHOOK:
            asyncio.run(_run_webhook())
        else:
            asyncio.run(_run_polling())
    except KeyboardInterrupt:
        LOGGER.info("🔌 Interrupted. Exiting...")
