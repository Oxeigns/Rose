"""Main entrypoint for the Rose Telegram bot."""

import asyncio
import json
import logging
import os
import sys
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client, idle

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
logging.getLogger("pyrogram").setLevel(logging.INFO)

# -------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    LOGGER.error("❌ API_ID, API_HASH, and BOT_TOKEN must be provided.")
    raise SystemExit(1)

API_ID = int(API_ID)

# -------------------------------------------------------------
# Bot Client with plugin support
# -------------------------------------------------------------
# IMPORTANT: 'Rose.plugins' must match the real directory structure.
app = Client(
    "rose_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
)


# -------------------------------------------------------------
# Delete webhook to enable polling
# -------------------------------------------------------------
def _delete_webhook() -> None:
    """Remove any webhook (if set) to enable polling mode."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        if not data.get("ok"):
            LOGGER.warning("⚠️ Failed to delete webhook: %s", data)
        else:
            LOGGER.info("✅ Webhook deleted successfully.")
    except Exception as e:
        LOGGER.warning("⚠️ Exception while deleting webhook: %s", e)


# -------------------------------------------------------------
# Bot lifecycle
# -------------------------------------------------------------
async def main() -> None:
    LOGGER.info("🚀 Starting Rose bot...")

    await asyncio.to_thread(_delete_webhook)

    try:
        await app.start()
    except Exception as e:
        LOGGER.exception("❌ Failed to start bot: %s", e)
        return

    handler_count = sum(len(g) for g in app.dispatcher.groups.values())
    LOGGER.info(
        "🔌 Loaded %s handler(s) across %s group(s)",
        handler_count,
        len(app.dispatcher.groups),
    )

    await init_db()
    LOGGER.info("✅ Rose bot is running. Awaiting events...")

    try:
        await idle()
    finally:
        LOGGER.info("🛑 Stopping bot...")
        await app.stop()
        LOGGER.info("✅ Bot stopped cleanly.")


# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("🔌 Interrupted. Exiting...")
