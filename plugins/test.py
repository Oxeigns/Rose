from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from modules.constants import PREFIXES
from utils.errors import catch_errors
import logging

LOGGER = logging.getLogger(__name__)

@catch_errors
async def test_cmd(client: Client, message: Message) -> None:
    LOGGER.debug("📩 /test received")
    if message.chat.type == "private":
        await message.reply_text("✅ Test command received!")
    else:
        await message.reply("📩 Check your PM for the test result.")
        try:
            await client.send_message(message.from_user.id, "✅ Test command received!")
        except Exception:
            await message.reply("❌ I can't message you. Please start me in PM first.")


def register(app: Client) -> None:
    app.add_handler(
        MessageHandler(test_cmd, filters.command("test", prefixes=PREFIXES)),
        group=0,
    )
