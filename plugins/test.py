from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("ping"))
async def ping_pong(client: Client, message: Message):
    await message.reply_text("pong")

@Client.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello, I am alive!")

@Client.on_message(filters.text & ~filters.command(["ping", "start"]))
async def echo_all(client: Client, message: Message):
    await message.reply_text(f"echo: {message.text}")
