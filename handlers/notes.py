from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.decorators import admin_required
from utils.db import get_conn, set_chat_setting, get_chat_setting
from buttons.notes import notes_panel

conn = get_conn()


def _get_note(chat_id: int, name: str):
    cur = conn.cursor()
    cur.execute('SELECT content FROM notes WHERE chat_id=? AND name=?', (chat_id, name.lower()))
    row = cur.fetchone()
    return row[0] if row else None


@Client.on_message(filters.command('save') & filters.group)
@admin_required
async def save_note(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /save <name> (reply or text)')
        return
    name = message.command[1].lower()
    if message.reply_to_message:
        content = message.reply_to_message.text or message.reply_to_message.caption
    else:
        if len(message.command) < 3:
            await message.reply('Provide note content.')
            return
        content = ' '.join(message.command[2:])
    cur = conn.cursor()
    cur.execute('REPLACE INTO notes(chat_id, name, content) VALUES(?,?,?)', (message.chat.id, name, content))
    conn.commit()
    await message.reply('Saved note.')


@Client.on_message(filters.command('clear') & filters.group)
@admin_required
async def clear_note(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /clear <name>')
        return
    name = message.command[1].lower()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE chat_id=? AND name=?', (message.chat.id, name))
    conn.commit()
    await message.reply('Note deleted.')


@Client.on_message(filters.command(['notes', 'saved']) & filters.group)
async def list_notes(client, message):
    cur = conn.cursor()
    cur.execute('SELECT name FROM notes WHERE chat_id=? ORDER BY name', (message.chat.id,))
    rows = cur.fetchall()
    if not rows:
        await message.reply('No notes in this chat.')
    else:
        text = '**Notes:**\n' + '\n'.join(f'- {n[0]}' for n in rows)
        await message.reply(text, reply_markup=notes_panel())


@Client.on_message(filters.command('clearall') & filters.group)
@admin_required
async def clear_all_notes(client, message):
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE chat_id=?', (message.chat.id,))
    conn.commit()
    await message.reply('All notes cleared.')


@Client.on_message(filters.command('privatenotes') & filters.group)
@admin_required
async def private_notes_toggle(client, message):
    current = get_chat_setting(message.chat.id, 'privatenotes', 'off')
    new = 'off' if current == 'on' else 'on'
    set_chat_setting(message.chat.id, 'privatenotes', new)
    await message.reply(f'Private notes are now {new}.')


@Client.on_message(filters.command('get') & filters.group)
async def get_note_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /get <name>')
        return
    name = message.command[1].lower()
    content = _get_note(message.chat.id, name)
    if content:
        if get_chat_setting(message.chat.id, 'privatenotes', 'off') == 'on':
            await client.send_message(message.from_user.id, content)
            await message.reply('Sent you the note in PM.')
        else:
            await message.reply(content)
    else:
        await message.reply('Note not found.')


@Client.on_message(filters.text & filters.group)
async def get_note_hash(client, message):
    if not message.text or not message.text.startswith('#'):
        return
    name = message.text[1:].split()[0].lower()
    content = _get_note(message.chat.id, name)
    if content:
        if get_chat_setting(message.chat.id, 'privatenotes', 'off') == 'on':
            await client.send_message(message.from_user.id, content)
        else:
            await message.reply(content)


@Client.on_callback_query(filters.regex('^notes:'))
async def notes_cb(client, query):
    data = query.data.split(':')[1]
    if data == 'example':
        await query.message.edit('Use `/save name` in reply to a message to save it.', reply_markup=notes_panel())
    elif data == 'format':
        await query.message.edit('Markdown and buttons are supported.', reply_markup=notes_panel())
    await query.answer()


def register(app: Client):
    pass
