import asyncio
import logging
import os

from dotenv import load_dotenv
from pyrogram import Client, idle

from handlers import register_all
from db import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
LOG = logging.getLogger(__name__)

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_NAME = os.getenv("SESSION_NAME", "rose_bot")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise RuntimeError("API_ID, API_HASH and BOT_TOKEN must be provided")

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def main():
    LOG.info("Starting bot...")
    await app.start()
    await init_db()
    await register_all(app)
    LOG.info("Bot started. Press Ctrl+C to stop.")
    await idle()
    await app.stop()
    LOG.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
