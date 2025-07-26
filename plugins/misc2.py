from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time

async def ping(client: Client, message: Message):
    start = time.monotonic()
    if message.chat.type == 'private':
        reply = await message.reply_text('Pong!')
        end = time.monotonic()
        await reply.edit_text(f'Pong! `{(end - start) * 1000:.0f}ms`', parse_mode='markdown')
    else:
        await message.reply("📩 Pong sent in PM.")
        end = time.monotonic()
        try:
            await client.send_message(
                message.from_user.id,
                f'Pong! `{(end - start) * 1000:.0f}ms`',
                parse_mode='markdown',
            )
        except Exception:
            await message.reply("❌ I can't message you. Please start me in PM first.")

async def echo(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/echo <text>`', parse_mode='markdown')
        return
    await message.reply_text(' '.join(message.command[1:]))


def register(app):
    app.add_handler(MessageHandler(ping, filters.command('ping', prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(echo, filters.command('echo', prefixes=PREFIXES)), group=0)
