from pyrogram import Client, filters
from pyrogram.types import Message
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting

# --- COMMANDS ---

@Client.on_message(filters.command("setwelcome") & filters.group)
@admin_required
async def set_welcome(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/setwelcome <message>`", parse_mode="markdown")
        return
    text = message.text.split(None, 1)[1]
    set_chat_setting(message.chat.id, "welcome", text)
    await message.reply_text("✅ Welcome message set.", parse_mode="markdown")

@Client.on_message(filters.command("setgoodbye") & filters.group)
@admin_required
async def set_goodbye(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/setgoodbye <message>`", parse_mode="markdown")
        return
    text = message.text.split(None, 1)[1]
    set_chat_setting(message.chat.id, "goodbye", text)
    await message.reply_text("👋 Goodbye message set.", parse_mode="markdown")

@Client.on_message(filters.command("greetings") & filters.group)
async def show_greetings(client: Client, message: Message):
    welcome = get_chat_setting(message.chat.id, "welcome", "Not set.")
    goodbye = get_chat_setting(message.chat.id, "goodbye", "Not set.")

    msg = f"**👋 Greetings Settings:**\n"
    msg += f"• **Welcome:** `{welcome}`\n"
    msg += f"• **Goodbye:** `{goodbye}`"
    await message.reply_text(msg, parse_mode="markdown")


# --- AUTOMATED HOOKS ---

@Client.on_message(filters.new_chat_members)
async def greet_new_members(client: Client, message: Message):
    text_template = get_chat_setting(message.chat.id, "welcome")
    if not text_template:
        return

    for user in message.new_chat_members:
        text = format_greeting(text_template, user, message.chat.title)
        await message.reply_text(text, parse_mode="markdown")

@Client.on_message(filters.left_chat_member)
async def farewell_user(client: Client, message: Message):
    text_template = get_chat_setting(message.chat.id, "goodbye")
    if not text_template:
        return

    user = message.left_chat_member
    text = format_greeting(text_template, user, message.chat.title)
    await message.reply_text(text, parse_mode="markdown")


# --- FORMATTER ---

def format_greeting(template: str, user, chat_title: str) -> str:
    first = user.first_name or ""
    mention = user.mention or f"[{first}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "N/A"

    return template.format(
        first=first,
        mention=mention,
        username=username,
        id=user.id,
        chat=chat_title,
    )
