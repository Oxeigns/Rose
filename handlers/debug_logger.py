import logging
from pyrogram import Client, filters
from pyrogram.types import Message

LOGGER = logging.getLogger(__name__)


def register(app: Client) -> None:
    @app.on_message(filters.group | filters.private, group=-2)
    async def log_all_messages(client: Client, message: Message) -> None:
        user_id = message.from_user.id if message.from_user else "unknown"
        username = (
            message.from_user.username
            if message.from_user and message.from_user.username
            else message.from_user.first_name
            if message.from_user
            else "unknown"
        )

        chat_id = message.chat.id if message.chat else "unknown"
        chat_title = message.chat.title if message.chat and message.chat.title else "Private Chat"
        msg_type = "Group" if message.chat and message.chat.type in ["group", "supergroup"] else "Private"

        text = message.text or message.caption or ""

        LOGGER.debug(
            "[%s] Message from %s (%s) in %s (%s): %s",
            msg_type,
            username,
            user_id,
            chat_title,
            chat_id,
            text.replace("\n", " "),
        )
