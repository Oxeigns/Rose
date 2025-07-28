from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import get_chat_setting, set_chat_setting
SUPPORTED_LANGUAGES = {'en': 'English 🇬🇧', 'hi': 'Hindi 🇮🇳', 'es': 'Spanish 🇪🇸', 'fr': 'French 🇫🇷', 'ar': 'Arabic 🇸🇦'}

async def show_languages(client: Client, message: Message):
    current = get_chat_setting(message.chat.id, 'lang', 'en')
    langs = '\n'.join((f'• `{code}` - {name}' for code, name in SUPPORTED_LANGUAGES.items()))
    await message.reply_text(f'**🌐 Current Language:** `{current}`\n\n**Available Languages:**\n{langs}\n\nTo change: `/setlang <code>`', parse_mode=ParseMode.MARKDOWN)

@admin_required
async def set_language(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/setlang <language_code>`', parse_mode=ParseMode.MARKDOWN)
        return
    code = message.command[1].lower()
    if code not in SUPPORTED_LANGUAGES:
        await message.reply_text('❌ Invalid language code. Use `/languages` to see available options.')
        return
    set_chat_setting(message.chat.id, 'lang', code)
    await message.reply_text(f'✅ Language set to `{SUPPORTED_LANGUAGES[code]}`', parse_mode=ParseMode.MARKDOWN)


def register(app):
    app.add_handler(MessageHandler(show_languages, filters.command('languages', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(set_language, filters.command('setlang', prefixes=PREFIXES) & filters.group), group=0)
