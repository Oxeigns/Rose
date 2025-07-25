from pyrogram import Client, filters
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
    await message.reply_text(f"echo: {message.text}")


def register(app):
    app.add_handler(MessageHandler(ping_pong, filters.command("ping")), group=0)
    app.add_handler(MessageHandler(start_message, filters.command("start")), group=0)
    app.add_handler(MessageHandler(echo_all, filters.text & ~filters.command(["ping", "start"])), group=0)
