"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
from pyrogram import Client
from dotenv import load_dotenv

from handlers import register_all
from db import init_db


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

# Load variables from .env if present
load_dotenv()

# Bot configuration with environment overrides
API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
SESSION_NAME = os.environ.get("SESSION_NAME", "rose_bot")

# Initialise the Pyrogram client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def main() -> None:
    """Load handlers and start the bot."""

    try:
        LOGGER.info("Initialising database ...")
        asyncio.run(init_db())
        LOGGER.info("Loading handlers ...")
        register_all(app)
    except Exception:
        LOGGER.exception("Failed to initialise bot")
        return

    LOGGER.info("Starting bot ...")
    try:
        app.run()
    except Exception:
        LOGGER.exception("Bot stopped due to an unexpected error")


if __name__ == "__main__":
    main()
