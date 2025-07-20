from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

async def is_admin(client: Client, message: Message, user_id: int) -> bool:
    if message.chat.type == "private":
        return True
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        return member.status in ("administrator", "creator")
    except UserNotParticipant:
        return False
    except Exception:
        return False
