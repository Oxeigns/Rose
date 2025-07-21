"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
from pyrogram import Client, idle
from dotenv import load_dotenv

from handlers import register_all
from db import init_db

# ------------------- Logging Setup -------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # 👈 Show all logs including message content
)
LOGGER = logging.getLogger(__name__)

# ------------------- Environment Variables -------------------
load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
SESSION_NAME = os.environ.get("SESSION_NAME", "rose_bot")

if (
    API_ID == 123456 or
    API_HASH == "YOUR_API_HASH" or
    BOT_TOKEN == "YOUR_BOT_TOKEN"
):
    LOGGER.error("❌ Missing API credentials. Please set them in the .env file.")
    raise SystemExit(1)

# ------------------- Pyrogram Client Setup -------------------
app = Client(
    name=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ------------------- Error Handler -------------------
def handle_exception(loop: asyncio.AbstractEventLoop, context: dict) -> None:
    """Log unhandled asyncio exceptions."""
    exc = context.get("exception")
    msg = context.get("message", "Unhandled exception occurred")
    LOGGER.error("Unhandled exception: %s", msg, exc_info=exc)

# ------------------- Bot Startup -------------------
async def main() -> None:
    try:
        await app.start()
        LOGGER.info("✅ Bot started and connected to Telegram")

        # Setup error handler
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(handle_exception)

        # Initialize database
        await init_db()
        LOGGER.info("📦 Database initialized")

        # Load all handlers
        await register_all(app)
        LOGGER.info("✅ All handlers registered")

        LOGGER.info("🤖 Bot is running...")
        await idle()

    except Exception as e:
        LOGGER.exception("🚨 Bot crashed due to an error")

    finally:
        await app.stop()
        LOGGER.info("🛑 Bot stopped gracefully")

# ------------------- Entry Point -------------------
if __name__ == "__main__":
    asyncio.run(main())
