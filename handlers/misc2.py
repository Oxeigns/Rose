from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time

# Simple misc commands

@Client.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    start = time.monotonic()
    reply = await message.reply_text("Pong!")
    end = time.monotonic()
    await reply.edit_text(f"Pong! `{(end - start) * 1000:.0f}ms`", parse_mode="markdown")

@Client.on_message(filters.command("echo"))
async def echo(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/echo <text>`", parse_mode="markdown")
        return
    await message.reply_text(" ".join(message.command[1:]))
