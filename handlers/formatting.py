from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler

async def formatting_help(client: Client, message: Message):
    text = """
**✨ Telegram Message Formatting Guide**

You can style your messages using Markdown or HTML formatting.

**Markdown Examples:**
• `*bold*` → *bold*
• `_italic_` → _italic_
• `` `code` `` → `code`
• `[title](https://example.com)` → [title](https://example.com)

**HTML Examples:**
• `<b>bold</b>` → <b>bold</b>
• `<i>italic</i>` → <i>italic</i>
• `<a href="https://example.com">Link</a>` → <a href="https://example.com">Link</a>
• `<code>code</code>` → <code>code</code>

__Make sure bots are configured to parse Markdown or HTML!__
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Telegram Formatting Docs", url="https://core.telegram.org/bots/api#formatting-options")
            ]
        ]
    )

    await message.reply_text(text, reply_markup=buttons, parse_mode="markdown")


def register(app: Client) -> None:
    app.add_handler(MessageHandler(formatting_help, filters.command("formatting")))
