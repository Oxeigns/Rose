"""Main entrypoint for the Rose Telegram bot."""

import asyncio
import importlib
import inspect
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import CallbackQuery, Message

from db import init_db


# -------------------------------------------------------------
# Logging setup: DEBUG to stdout/debug.log and ERROR to error.log
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

# Separate handler to capture only errors
error_handler = logging.FileHandler(LOG_DIR / "error.log", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(error_handler)

LOGGER = logging.getLogger(__name__)


# -------------------------------------------------------------
# Environment loading and validation
# -------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME", "rose_bot")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    LOGGER.error("API_ID, API_HASH and BOT_TOKEN must be provided")
    raise SystemExit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    LOGGER.error("API_ID must be an integer")
    raise SystemExit(1)


# -------------------------------------------------------------
# Client initialization
# -------------------------------------------------------------
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# -------------------------------------------------------------
# Global logging of all messages and callback queries
# -------------------------------------------------------------
async def _log_message(client: Client, message: Message) -> None:
    user = message.from_user
    chat = message.chat
    chat_title = chat.title if chat and chat.title else "Private"
    msg_type = "Group" if chat and chat.type in ("group", "supergroup") else "Private"
    text = message.text or message.caption or ""
    LOGGER.debug(
        "[%s] %s (%s) in %s (%s): %s",
        msg_type,
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat_title,
        chat.id if chat else "N/A",
        text.replace("\n", " "),
    )

async def _log_query(client: Client, query: CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat if query.message else None
    chat_title = chat.title if chat and chat.title else "Private"
    msg_type = "Group" if chat and chat.type in ("group", "supergroup") else "Private"
    LOGGER.debug(
        "[Callback %s] %s (%s) in %s (%s): %s",
        msg_type,
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat_title,
        chat.id if chat else "N/A",
        query.data,
    )


# -------------------------------------------------------------
# Dynamic handler loader
# -------------------------------------------------------------
async def load_handlers(app: Client) -> None:
    """Import all modules from handlers/ and call their register() function."""
    handlers_path = Path(__file__).parent / "handlers"
    for file in sorted(handlers_path.glob("*.py")):
        if file.stem.startswith("_") or file.stem == "__init__":
            continue
        module_name = f"handlers.{file.stem}"
        try:
            module = importlib.import_module(module_name)
        except Exception as imp_err:
            LOGGER.exception("Failed importing %s: %s", module_name, imp_err)
            continue
        register_fn = getattr(module, "register", None)
        if not register_fn:
            LOGGER.warning("No register() in %s", module_name)
            continue
        try:
            if inspect.iscoroutinefunction(register_fn):
                await register_fn(app)
            else:
                register_fn(app)
            LOGGER.info("Loaded handlers from %s", module_name)
        except Exception as reg_err:
            LOGGER.exception("Error in register() of %s: %s", module_name, reg_err)


# -------------------------------------------------------------
# Bot startup/shutdown
# -------------------------------------------------------------
async def main() -> None:
    LOGGER.info("Starting bot...")
    await app.start()
    await init_db()
    # Register global log handlers
    app.add_handler(MessageHandler(_log_message, filters.group | filters.private), group=-2)
    app.add_handler(CallbackQueryHandler(_log_query), group=-2)
    await load_handlers(app)
    LOGGER.info("Bot started. Press Ctrl+C to stop.")
    await idle()
    LOGGER.info("Stopping bot...")
    await app.stop()
    LOGGER.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())

