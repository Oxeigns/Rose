from pyrogram import Client, filters
from utils.decorators import admin_required
import time

FLOOD_LIMIT = {}
MSG_COUNT = {}

@Client.on_message(filters.command('setflood') & filters.group)
@admin_required
async def setflood(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /setflood <count>')
        return
    try:
        count = int(message.command[1])
    except ValueError:
        await message.reply('Give a number.')
        return
    FLOOD_LIMIT[message.chat.id] = count
    await message.reply(f'Set flood limit to {count}')

@Client.on_message(filters.text & filters.group)
async def check_flood(client, message):
    limit = FLOOD_LIMIT.get(message.chat.id)
    if not limit:
        return
    key = (message.chat.id, message.from_user.id)
    last_time, count = MSG_COUNT.get(key, (0,0))
    now = time.time()
    if now - last_time > 5:
        count = 0
    count += 1
    MSG_COUNT[key] = (now, count)
    if count > limit:
        await message.delete()
