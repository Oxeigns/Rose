from pyrogram import Client, filters
from pyrogram.types import Message
from utils.decorators import admin_required
from utils.db import get_chat_setting, set_chat_setting

# Define your available languages
SUPPORTED_LANGUAGES = {
    "en": "English 🇬🇧",
    "hi": "Hindi 🇮🇳",
    "es": "Spanish 🇪🇸",
    "fr": "French 🇫🇷",
    "ar": "Arabic 🇸🇦",
    # Add more as needed
}

@Client.on_message(filters.command("languages") & filters.group)
async def show_languages(client: Client, message: Message):
    current = get_chat_setting(message.chat.id, "lang", "en")
    langs = "\n".join(f"• `{code}` - {name}" for code, name in SUPPORTED_LANGUAGES.items())
    await message.reply_text(
        f"**🌐 Current Language:** `{current}`\n\n"
        f"**Available Languages:**\n{langs}\n\n"
        "To change: `/setlang <code>`",
        parse_mode="markdown"
    )

@Client.on_message(filters.command("setlang") & filters.group)
@admin_required
async def set_language(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/setlang <language_code>`", parse_mode="markdown")
        return

    code = message.command[1].lower()
    if code not in SUPPORTED_LANGUAGES:
        await message.reply_text("❌ Invalid language code. Use `/languages` to see available options.")
        return

    set_chat_setting(message.chat.id, "lang", code)
    await message.reply_text(f"✅ Language set to `{SUPPORTED_LANGUAGES[code]}`", parse_mode="markdown")
