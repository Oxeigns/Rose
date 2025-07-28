from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler

async def formatting_help(client: Client, message: Message):
    text = '\n**✨ Telegram Message Formatting Guide**\n\nYou can style your messages using Markdown or HTML formatting.\n\n**Markdown Examples:**\n• `*bold*` → *bold*\n• `_italic_` → _italic_\n• `` `code` `` → `code`\n• `[title](https://example.com)` → [title](https://example.com)\n\n**HTML Examples:**\n• `<b>bold</b>` → <b>bold</b>\n• `<i>italic</i>` → <i>italic</i>\n• `<a href="https://example.com">Link</a>` → <a href="https://example.com">Link</a>\n• `<code>code</code>` → <code>code</code>\n\n__Make sure bots are configured to parse Markdown or HTML!__\n'
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton('📚 Telegram Formatting Docs', url='https://core.telegram.org/bots/api#formatting-options')]])
    await message.reply_text(text, reply_markup=buttons, parse_mode=ParseMode.MARKDOWN)


def register(app):
    app.add_handler(MessageHandler(formatting_help, filters.command('formatting', prefixes=PREFIXES)), group=0)
