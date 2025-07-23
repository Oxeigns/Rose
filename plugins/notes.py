from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.decorators import admin_required
from utils.db import get_conn, set_chat_setting, get_chat_setting
conn = get_conn()

def notes_panel():
    return InlineKeyboardMarkup([[InlineKeyboardButton('💾 Save Example', callback_data='notes:example')], [InlineKeyboardButton('🖍 Formatting', callback_data='notes:format')]])

def _get_note(chat_id: int, name: str):
    cur = conn.cursor()
    cur.execute('SELECT content FROM notes WHERE chat_id=? AND name=?', (chat_id, name.lower()))
    row = cur.fetchone()
    return row[0] if row else None

@admin_required
async def save_note(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply('Usage: `/save <name>` (reply or give text)', parse_mode='markdown')
        return
    name = message.command[1].lower()
    if message.reply_to_message:
        content = message.reply_to_message.text or message.reply_to_message.caption
    else:
        if len(message.command) < 3:
            await message.reply('Provide note content after the name.')
            return
        content = ' '.join(message.command[2:])
    cur = conn.cursor()
    cur.execute('REPLACE INTO notes(chat_id, name, content) VALUES(?,?,?)', (message.chat.id, name, content))
    conn.commit()
    await message.reply('✅ Saved note.')

@admin_required
async def clear_note(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply('Usage: `/clear <name>`', parse_mode='markdown')
        return
    name = message.command[1].lower()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE chat_id=? AND name=?', (message.chat.id, name))
    conn.commit()
    await message.reply('🗑️ Note deleted.')

async def list_notes(client: Client, message: Message):
    cur = conn.cursor()
    cur.execute('SELECT name FROM notes WHERE chat_id=? ORDER BY name', (message.chat.id,))
    rows = cur.fetchall()
    if not rows:
        await message.reply('❌ No notes found in this chat.')
    else:
        text = '**📝 Saved Notes:**\n' + '\n'.join((f'• `{n[0]}`' for n in rows))
        await message.reply(text, reply_markup=notes_panel(), parse_mode='markdown')

@admin_required
async def clear_all_notes(client: Client, message: Message):
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE chat_id=?', (message.chat.id,))
    conn.commit()
    await message.reply('🗑️ All notes cleared.')

@admin_required
async def private_notes_toggle(client: Client, message: Message):
    current = get_chat_setting(message.chat.id, 'privatenotes', 'off')
    new = 'off' if current == 'on' else 'on'
    set_chat_setting(message.chat.id, 'privatenotes', new)
    await message.reply(f'🔒 Private notes are now `{new}`.', parse_mode='markdown')

async def get_note_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply('Usage: `/get <name>`', parse_mode='markdown')
        return
    name = message.command[1].lower()
    content = _get_note(message.chat.id, name)
    if content:
        if get_chat_setting(message.chat.id, 'privatenotes', 'off') == 'on':
            await client.send_message(message.from_user.id, content)
            await message.reply('📬 Sent the note in your PM.')
        else:
            await message.reply(content)
    else:
        await message.reply('❌ Note not found.')

async def get_note_hash(client: Client, message: Message):
    if not message.text or not message.text.startswith('#'):
        return
    name = message.text[1:].split()[0].lower()
    content = _get_note(message.chat.id, name)
    if content:
        if get_chat_setting(message.chat.id, 'privatenotes', 'off') == 'on':
            await client.send_message(message.from_user.id, content)
        else:
            await message.reply(content)

async def notes_cb(client: Client, query: CallbackQuery):
    data = query.data.split(':')[1]
    if data == 'example':
        await query.message.edit_text('📌 To save a note:\nReply to a message and use `/save keyword`\nOr `/save keyword content`.', reply_markup=notes_panel(), parse_mode='markdown')
    elif data == 'format':
        await query.message.edit_text('**📎 Formatting Guide**\n- Markdown supported\n- Buttons via `[text](url)` allowed.', reply_markup=notes_panel(), parse_mode='markdown')
    await query.answer()


def register(app):
    app.add_handler(MessageHandler(save_note, filters.command('save') & filters.group), group=0)
    app.add_handler(MessageHandler(clear_note, filters.command('clear') & filters.group), group=0)
    app.add_handler(MessageHandler(list_notes, filters.command(['notes', 'saved']) & filters.group), group=0)
    app.add_handler(MessageHandler(clear_all_notes, filters.command('clearall') & filters.group), group=0)
    app.add_handler(MessageHandler(private_notes_toggle, filters.command('privatenotes') & filters.group), group=0)
    app.add_handler(MessageHandler(get_note_cmd, filters.command('get') & filters.group), group=0)
    app.add_handler(MessageHandler(get_note_hash, filters.text & filters.group), group=0)
    app.add_handler(CallbackQueryHandler(notes_cb, filters.regex('^notes:(?!open$)')), group=0)
