"""Main entrypoint for the Rose Telegram bot."""

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client, idle
import json
import urllib.request

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
plugins_root = Path(__file__).resolve().parent / "plugins"
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    plugins=None,
)

def load_plugins() -> None:
    """Load all plugin modules and log the number of handlers."""
    app.plugins = {"root": str(plugins_root)}
    app.load_plugins()
    total = sum(len(g) for g in app.dispatcher.groups.values())
    LOGGER.info("Loaded %d handlers from %s", total, plugins_root)
    app.plugins = None

# -------------------------------------------------------------

def _delete_webhook() -> None:
    """Remove any existing webhook using Telegram's Bot API."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        if not data.get("ok"):
            LOGGER.warning("Failed to delete webhook: %s", data)
        else:
            LOGGER.info("Deleted existing webhook")
    except Exception as exc:
        LOGGER.warning("Error deleting webhook: %s", exc)

# -------------------------------------------------------------
# Bot Lifecycle
# -------------------------------------------------------------
async def main() -> None:
    LOGGER.info("🚀 Starting Rose bot...")
    load_plugins()

    # Remove any webhook to enable polling with getUpdates
    await asyncio.to_thread(_delete_webhook)
    await app.start()
    await init_db()

    LOGGER.info("✅ Bot started. Waiting for events...")
    await idle()
    LOGGER.info("🛑 Bot stopped. Cleaning up...")
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Interrupted. Exiting...")
