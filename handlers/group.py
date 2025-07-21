import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.errors import catch_errors
from db.broadcast import add_user, add_group, remove_group

logger = logging.getLogger(__name__)

def register(app: Client) -> None:
    # ✅ /start used in private chat
    @app.on_message(filters.command("start") & filters.private)
    @catch_errors
    async def start_in_private(client: Client, message: Message):
        logger.info("📥 /start by user %s in PM", message.from_user.id)
        await add_user(message.from_user.id)

    # ✅ Bot added to a group
    @app.on_message(filters.new_chat_members & filters.group)
    @catch_errors
    async def bot_added(client: Client, message: Message):
        me = await client.get_me()
        if any(member.id == me.id for member in message.new_chat_members):
            logger.info("➕ Bot added to group %s", message.chat.id)
            await add_group(message.chat.id)

    # ✅ Bot removed from a group
    @app.on_message(filters.left_chat_member & filters.group)
    @catch_errors
    async def bot_removed(client: Client, message: Message):
        me = await client.get_me()
        if message.left_chat_member and message.left_chat_member.id == me.id:
            logger.info("➖ Bot removed from group %s", message.chat.id)
            await remove_group(message.chat.id)
