from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.errors import catch_errors


@catch_errors
async def ping_pong(client: Client, message: Message):
    await message.reply_text("pong")


@catch_errors
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello, I am alive!")


@catch_errors
async def echo_all(client: Client, message: Message):
    # Self-messages (bot ke khud ke messages) ko ignore karo
    if message.from_user and message.from_user.is_self:
        return

    # Optionally: Agar reply kisi bot message par hai to ignore
    if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.is_self:
        return

    await message.reply_text(f"echo: {message.text}")


def register(app):
    app.add_handler(MessageHandler(ping_pong, filters.command("ping", prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(start_message, filters.command("start", prefixes=PREFIXES)), group=0)
    # echo_all ko sab par chalana hai but commands ko exclude kar rahe hain
    app.add_handler(
        MessageHandler(
            echo_all,
            filters.text & ~filters.command(["ping", "start"], prefixes=PREFIXES)
        ),
        group=0
    )
