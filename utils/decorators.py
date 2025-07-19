from functools import wraps
from pyrogram.types import Message
from pyrogram import Client

from .db import get_conn

async def user_is_admin(client: Client, message: Message) -> bool:
    if message.chat.type == 'private':
        return True
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ("administrator", "creator")

def admin_required(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        if not await user_is_admin(client, message):
            await message.reply("You need to be an admin to do that.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper

def is_admin(func):
    """Decorator to allow only admins to run a command."""
    return admin_required(func)
