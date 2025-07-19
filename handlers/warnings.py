from pyrogram import Client, filters
from utils.decorators import admin_required
from utils.db import get_conn
import time

conn = get_conn()

@Client.on_message(filters.command('warn') & filters.group)
@admin_required
async def warn(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to warn.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    cur = conn.cursor()
    cur.execute('SELECT warn_count FROM warnings WHERE user_id=? AND chat_id=?', (user_id, chat_id))
    row = cur.fetchone()
    count = row[0] + 1 if row else 1
    if row:
        cur.execute('UPDATE warnings SET warn_count=?, timestamp=? WHERE user_id=? AND chat_id=?', (count, int(time.time()), user_id, chat_id))
    else:
        cur.execute('INSERT INTO warnings(user_id, chat_id, warn_count, timestamp) VALUES(?,?,?,?)', (user_id, chat_id, count, int(time.time())))
    conn.commit()
    await message.reply(f'Warned. Total warns: {count}')

@Client.on_message(filters.command('warns') & filters.group)
async def warns(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    chat_id = message.chat.id
    cur = conn.cursor()
    cur.execute('SELECT warn_count FROM warnings WHERE user_id=? AND chat_id=?', (user_id, chat_id))
    row = cur.fetchone()
    count = row[0] if row else 0
    await message.reply(f'Warn count: {count}')

@Client.on_message(filters.command('resetwarns') & filters.group)
@admin_required
async def resetwarns(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        await message.reply('Reply to a user to reset warns.')
        return
    chat_id = message.chat.id
    cur = conn.cursor()
    cur.execute('DELETE FROM warnings WHERE user_id=? AND chat_id=?', (user_id, chat_id))
    conn.commit()
    await message.reply('Warns reset.')
