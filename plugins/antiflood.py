from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
import time
FLOOD_LIMIT = {}
MSG_COUNT = {}

@Client.on_message(filters.command('setflood') & filters.group)
@admin_required
async def set_flood_limit(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: /setflood <count>')
        return
    try:
        count = int(message.command[1])
        if count < 1:
            raise ValueError
    except ValueError:
        await message.reply_text('Please provide a positive number.')
        return
    FLOOD_LIMIT[message.chat.id] = count
    await message.reply_text(f'✅ Flood limit set to `{count}` messages per 5 seconds.')

@Client.on_message(filters.command('flood') & filters.group)
@admin_required
async def get_flood_limit(client: Client, message: Message):
    limit = FLOOD_LIMIT.get(message.chat.id)
    if limit:
        await message.reply_text(f'🚰 Current flood limit: `{limit}` messages / 5s')
    else:
        await message.reply_text('🚫 No flood limit is currently set for this chat.')

@Client.on_message(filters.text & filters.group & ~filters.service)
async def flood_checker(client: Client, message: Message):
    limit = FLOOD_LIMIT.get(message.chat.id)
    if not limit or not message.from_user:
        return
    key = (message.chat.id, message.from_user.id)
    last_time, count = MSG_COUNT.get(key, (0, 0))
    now = time.time()
    if now - last_time > 5:
        count = 1
    else:
        count += 1
    MSG_COUNT[key] = (now, count)
    if count > limit:
        try:
            await message.delete()
        except Exception:
            pass
