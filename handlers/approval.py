from pyrogram import Client, filters
from pyrogram.types import Message
from utils.decorators import admin_required

# Temporary in-memory store (use DB in production)
APPROVED_USERS = {}  # chat_id: set(user_ids)

def is_approved(chat_id: int, user_id: int) -> bool:
    return user_id in APPROVED_USERS.get(chat_id, set())

@Client.on_message(filters.command("approve") & filters.group)
@admin_required
async def approve_user(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a user to approve them.")
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    APPROVED_USERS.setdefault(chat_id, set()).add(user_id)
    await message.reply_text(f"✅ Approved [{user_id}](tg://user?id={user_id}).", parse_mode="markdown")

@Client.on_message(filters.command("unapprove") & filters.group)
@admin_required
async def unapprove_user(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a user to unapprove them.")
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    APPROVED_USERS.setdefault(chat_id, set()).discard(user_id)
    await message.reply_text(f"🚫 Unapproved [{user_id}](tg://user?id={user_id}).", parse_mode="markdown")

@Client.on_message(filters.command("approved") & filters.group)
@admin_required
async def list_approved(client: Client, message: Message):
    chat_id = message.chat.id
    users = APPROVED_USERS.get(chat_id, set())
    
    if not users:
        await message.reply_text("No users are currently approved.")
        return

    text = "**✅ Approved Users:**\n"
    for user_id in users:
        text += f"- [User](tg://user?id={user_id}) (`{user_id}`)\n"
    
    await message.reply_text(text, parse_mode="markdown")

@Client.on_message(filters.command("clearapproved") & filters.group)
@admin_required
async def clear_approved(client: Client, message: Message):
    chat_id = message.chat.id
    APPROVED_USERS[chat_id] = set()
    await message.reply_text("✅ All approved users have been cleared.")
