from pyrogram import Client, filters
from utils.decorators import admin_required
from utils.db import get_conn

conn = get_conn()

@Client.on_message(filters.command('save') & filters.group)
@admin_required
async def save(client, message):
    if len(message.command) < 2 or not message.reply_to_message:
        await message.reply('Usage: /save note_name (reply to message)')
        return
    name = message.command[1]
    content = message.reply_to_message.text or message.reply_to_message.caption
    if not content:
        await message.reply('No text to save.')
        return
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE chat_id=? AND name=?', (message.chat.id, name))
    cur.execute('INSERT INTO notes(chat_id, name, content) VALUES(?,?,?)', (message.chat.id, name, content))
    conn.commit()
    await message.reply('Saved note.')

@Client.on_message(filters.command('get') & filters.group)
async def get_note(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /get note_name')
        return
    name = message.command[1]
    cur = conn.cursor()
    cur.execute('SELECT content FROM notes WHERE chat_id=? AND name=?', (message.chat.id, name))
    row = cur.fetchone()
    if row:
        await message.reply(row[0])
    else:
        await message.reply('Note not found.')
