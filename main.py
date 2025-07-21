"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
from pyrogram import Client, idle
from pyrogram.errors import PeerIdInvalid
from dotenv import load_dotenv

from handlers import register_all
from db import init_db
from config import LOG_GROUP_ID
from utils.markdown import escape_markdown

# ------------------- Logging Setup -------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
LOGGER = logging.getLogger(__name__)

# ------------------- Environment ---------------------
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
    LOGGER.error("❌ Missing API credentials. Set them in .env.")
    raise SystemExit(1)

# ------------------- Pyrogram Client -------------------
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ------------------- Logging to Group ------------------
async def send_log(text: str) -> None:
    if not LOG_GROUP_ID:
        return
    try:
        await app.send_message(LOG_GROUP_ID, text)
    except PeerIdInvalid:
        LOGGER.warning("LOG_GROUP_ID is invalid. Check config.")
    except Exception as log_e:
        LOGGER.warning("Log group send failed: %s", log_e)

# ------------------- Global Error Handler --------------
def handle_exception(loop: asyncio.AbstractEventLoop, context: dict) -> None:
    """Log and report unhandled exceptions in the asyncio loop."""
    exception = context.get("exception")
    message = context.get("message", "Unhandled exception")
    LOGGER.error("Unhandled exception: %s", message, exc_info=exception)
    err_text = str(exception or message)
    if loop.is_running():
        loop.create_task(
            send_log(f"🚨 Unhandled exception: `{escape_markdown(err_text)}`")
        )

# ------------------- Bot Runner ------------------------
async def main() -> None:
    try:
        await app.start()  # 🔄 Start client first
        LOGGER.info("🔗 Connected to Telegram")

        # Report any unhandled exceptions through our custom handler
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(handle_exception)

        await init_db()
        LOGGER.info("📦 Database initialized")

        await register_all(app)
        LOGGER.info("✅ Handlers registered")

        await send_log("✅ Bot deployed and running.")
        await idle()

    except Exception as e:
        LOGGER.exception("Bot crashed unexpectedly")
        await send_log(f"🚨 Bot crashed: `{escape_markdown(str(e))}`")

    finally:
        await app.stop()
        LOGGER.info("Bot stopped gracefully.")

# ------------------- Entry Point ------------------------
if __name__ == "__main__":
    asyncio.run(main())
