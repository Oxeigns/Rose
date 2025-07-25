from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
CONNECTIONS = {}

@admin_required
async def connect_group(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    CONNECTIONS[user_id] = chat_id
    await message.reply_text('🔗 Group connected! You can now use group commands in private chat.')

@admin_required
async def disconnect_group(client: Client, message: Message):
    user_id = message.from_user.id
    if CONNECTIONS.get(user_id) == message.chat.id:
        del CONNECTIONS[user_id]
        await message.reply_text('❌ Disconnected from this group.')
    else:
        await message.reply_text('You’re not connected to this group.')

async def show_connection(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = CONNECTIONS.get(user_id)
    if chat_id:
        try:
            chat = await client.get_chat(chat_id)
            await message.reply_text(f'🔌 Currently connected to: `{chat.title}` (`{chat.id}`)', parse_mode='markdown')
        except Exception:
            await message.reply_text('⚠️ Could not access connected group.')
    else:
        await message.reply_text('🚫 You are not connected to any group. Use `/connect` in a group to link it.')

def get_user_connection(user_id: int) -> int | None:
    return CONNECTIONS.get(user_id)


def register(app):
    app.add_handler(MessageHandler(connect_group, filters.command('connect', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(disconnect_group, filters.command('disconnect', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(show_connection, filters.command('connections', prefixes=PREFIXES) & filters.private), group=0)