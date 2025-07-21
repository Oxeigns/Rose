from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time

# Simple misc commands

async def ping(client: Client, message: Message):
    start = time.monotonic()
    reply = await message.reply_text("Pong!")
    end = time.monotonic()
    await reply.edit_text(f"Pong! `{(end - start) * 1000:.0f}ms`", parse_mode="markdown")

async def echo(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/echo <text>`", parse_mode="markdown")
        return
    await message.reply_text(" ".join(message.command[1:]))


def register(app: Client) -> None:
    app.add_handler(MessageHandler(ping, filters.command("ping")))
    app.add_handler(MessageHandler(echo, filters.command("echo")))
