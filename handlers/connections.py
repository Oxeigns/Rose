from pyrogram import Client, filters
from pyrogram.types import Message
from utils.decorators import admin_required

# Temporary in-memory map (user_id: chat_id)
CONNECTIONS = {}

@Client.on_message(filters.command("connect") & filters.group)
@admin_required
async def connect_group(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    CONNECTIONS[user_id] = chat_id
    await message.reply_text("🔗 Group connected! You can now use group commands in private chat.")

@Client.on_message(filters.command("disconnect") & filters.group)
@admin_required
async def disconnect_group(client: Client, message: Message):
    user_id = message.from_user.id
    if CONNECTIONS.get(user_id) == message.chat.id:
        del CONNECTIONS[user_id]
        await message.reply_text("❌ Disconnected from this group.")
    else:
        await message.reply_text("You’re not connected to this group.")

@Client.on_message(filters.command("connections") & filters.private)
async def show_connection(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = CONNECTIONS.get(user_id)

    if chat_id:
        try:
            chat = await client.get_chat(chat_id)
            await message.reply_text(f"🔌 Currently connected to: `{chat.title}` (`{chat.id}`)", parse_mode="markdown")
        except Exception:
            await message.reply_text("⚠️ Could not access connected group.")
    else:
        await message.reply_text("🚫 You are not connected to any group. Use `/connect` in a group to link it.")

# Utility to get connected group from a user in private
def get_user_connection(user_id: int) -> int | None:
    return CONNECTIONS.get(user_id)
