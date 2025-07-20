"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
from pyrogram import Client, idle
from dotenv import load_dotenv

from handlers import register_all
from db import init_db
from config import LOG_GROUP_ID
from utils.markdown import escape_markdown


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

# Abort early if credentials were not provided
if (
    API_ID == 123456 or
    API_HASH == "YOUR_API_HASH" or
    BOT_TOKEN == "YOUR_BOT_TOKEN"
):
    LOGGER.error(
        "Missing API credentials. Please populate a .env file "
        "or set the API_ID, API_HASH and BOT_TOKEN environment variables."
    )
    raise SystemExit(1)

# Initialise the Pyrogram client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def main() -> None:
    """Load handlers and start the bot."""

    try:
        LOGGER.info("Initialising database ...")
        await init_db()
        LOGGER.info("Loading handlers ...")
        register_all(app)
    except Exception as e:
        LOGGER.exception("Failed to initialise bot")
        if LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    f"🚨 Bot failed to initialise: `{escape_markdown(str(e))}`",
                    parse_mode="markdown",
                )
            except Exception as log_e:
                LOGGER.warning("Failed to send error to LOG_GROUP_ID: %s", log_e)
        return

    LOGGER.info("Starting bot ...")
    try:
        await app.start()
        if LOG_GROUP_ID:
            try:
                await app.send_message(LOG_GROUP_ID, "✅ Bot deployed and running.")
            except Exception as log_e:
                LOGGER.warning("Failed to send startup message to LOG_GROUP_ID: %s", log_e)
        await idle()
    except Exception as e:
        LOGGER.exception("Bot stopped due to an unexpected error")
        if LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    f"🚨 Bot crashed: `{escape_markdown(str(e))}`",
                    parse_mode="markdown",
                )
            except Exception as log_e:
                LOGGER.warning("Failed to send crash message to LOG_GROUP_ID: %s", log_e)
    finally:
        if app.is_connected:
            await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
