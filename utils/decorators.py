from functools import wraps
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.errors import UserNotParticipant

async def user_is_admin(client: Client, message: Message) -> bool:
    if message.chat.type == 'private':
        return True
    if not message.from_user:
        return False
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ("administrator", "creator")
    except UserNotParticipant:
        return False
    except Exception:
        return False

def admin_required(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        if not await user_is_admin(client, message):
            await message.reply("❌ You need to be an admin to use this command.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper

def is_admin(func):
    """Alias for admin_required decorator."""
    return admin_required(func)
