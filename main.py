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
from pyrogram.types import Message, CallbackQuery

from handlers import register_all as register_handlers
from db import init_db

# -------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
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

# -------------------------------------------------------------
# Load environment
# -------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME", "rose_bot")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    LOGGER.error("API_ID, API_HASH and BOT_TOKEN must be provided.")
    raise SystemExit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    LOGGER.error("API_ID must be an integer.")
    raise SystemExit(1)

# -------------------------------------------------------------
# Bot Client
# -------------------------------------------------------------
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    plugins={"root": "plugins"}  # Optional if you're using a plugins folder
)

# -------------------------------------------------------------
# Debug Logging Handlers
# -------------------------------------------------------------
async def _log_message(client: Client, message: Message) -> None:
    user = message.from_user
    chat = message.chat
    LOGGER.debug(
        "[%s] %s (%s) in %s (%s): %s",
        "Group" if chat.type in ("group", "supergroup") else "Private",
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat.title if chat else "N/A",
        chat.id if chat else "N/A",
        message.text or message.caption or "",
    )

async def _log_query(client: Client, query: CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat if query.message else None
    LOGGER.debug(
        "[Callback %s] %s (%s) in %s (%s): %s",
        "Group" if chat and chat.type in ("group", "supergroup") else "Private",
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat.title if chat else "N/A",
        chat.id if chat else "N/A",
        query.data,
    )

# -------------------------------------------------------------
# Dynamic Module Loader
# -------------------------------------------------------------
async def load_modules(app: Client) -> None:
    """Dynamically import all modules in 'modules/' and run register() if present."""
    modules_path = Path(__file__).parent / "modules"
    if not modules_path.exists():
        LOGGER.warning("⚠️ No 'modules' folder found.")
        return

    for file in sorted(modules_path.glob("*.py")):
        if file.stem.startswith("_") or file.stem == "__init__":
            continue

        module_name = f"modules.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            LOGGER.debug("📦 Imported module: %s", module_name)
        except Exception as e:
            LOGGER.exception("❌ Failed to import %s: %s", module_name, e)
            continue

        register_fn = getattr(module, "register", None)
        if register_fn:
            try:
                if inspect.iscoroutinefunction(register_fn):
                    await register_fn(app)
                else:
                    register_fn(app)
                LOGGER.info("✅ Registered module: %s", module_name)
            except Exception as e:
                LOGGER.exception("❌ Error in %s.register(): %s", module_name, e)

# -------------------------------------------------------------
# Main Bot Lifecycle
# -------------------------------------------------------------
async def main() -> None:
    LOGGER.info("🚀 Starting Rose bot...")

    await app.start()
    await init_db()

    # Logging handlers
    app.add_handler(MessageHandler(_log_message, filters.group | filters.private), group=-2)
    app.add_handler(CallbackQueryHandler(_log_query), group=-2)

    # Load all handlers and modules
    await register_handlers(app)
    await load_modules(app)

    # Catch-all debug
    @app.on_message(filters.all)
    async def catch_all(client, message):
        LOGGER.debug("⚠️ Catch-all received: %s", message.text or message.caption)

    LOGGER.info("✅ Bot started. Waiting for events...")
    await idle()
    LOGGER.info("🛑 Bot stopped. Cleaning up...")
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Interrupted. Exiting...")
