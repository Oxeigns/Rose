from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
BLOCKLIST = {}

@admin_required
async def add_blocked_word(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/addblock <word>`', parse_mode='markdown')
        return
    word = message.command[1].lower()
    chat_id = message.chat.id
    BLOCKLIST.setdefault(chat_id, set()).add(word)
    await message.reply_text(f'🚫 Added `{word}` to blocklist.', parse_mode='markdown')

@admin_required
async def remove_blocked_word(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/unblock <word>`', parse_mode='markdown')
        return
    word = message.command[1].lower()
    chat_id = message.chat.id
    BLOCKLIST.setdefault(chat_id, set()).discard(word)
    await message.reply_text(f'✅ Removed `{word}` from blocklist.', parse_mode='markdown')

@admin_required
async def show_blocklist(client: Client, message: Message):
    chat_id = message.chat.id
    words = BLOCKLIST.get(chat_id, set())
    if not words:
        await message.reply_text('✅ Blocklist is empty.')
        return
    text = '**🚫 Blocked Words:**\n'
    for word in sorted(words):
        text += f'• `{word}`\n'
    await message.reply_text(text, parse_mode='markdown')

@admin_required
async def clear_blocklist(client: Client, message: Message):
    chat_id = message.chat.id
    BLOCKLIST[chat_id] = set()
    await message.reply_text('🧹 Blocklist has been cleared.')

async def auto_delete_blocked(client: Client, message: Message):
    chat_id = message.chat.id
    words = BLOCKLIST.get(chat_id, set())
    if not words or not message.text:
        return
    lowered = message.text.lower()
    for word in words:
        if word in lowered:
            try:
                await message.delete()
            except Exception:
                pass
            break


def register(app):
    app.add_handler(MessageHandler(add_blocked_word, filters.command('addblock') & filters.group), group=0)
    app.add_handler(MessageHandler(remove_blocked_word, filters.command('unblock') & filters.group), group=0)
    app.add_handler(MessageHandler(show_blocklist, filters.command('blocklist') & filters.group), group=0)
    app.add_handler(MessageHandler(clear_blocklist, filters.command('clearblocklist') & filters.group), group=0)
    app.add_handler(MessageHandler(auto_delete_blocked, filters.text & filters.group & ~filters.service), group=0)
