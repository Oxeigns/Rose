from pyrogram import Client, filters
from pyrogram.types import Message

async def ping_pong(client: Client, message: Message):
    await message.reply_text("pong")

async def start_message(client: Client, message: Message):
    await message.reply_text("Hello, I am alive!")

async def echo_all(client: Client, message: Message):
    await message.reply_text(f"echo: {message.text}")


def register(app):
    app.add_handler(MessageHandler(ping_pong, filters.command("ping")), group=0)
    app.add_handler(MessageHandler(start_message, filters.command("start")), group=0)
    app.add_handler(MessageHandler(echo_all, filters.text & ~filters.command(["ping", "start"])), group=0)
