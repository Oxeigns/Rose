import logging
from pyrogram import Client, filters
from pyrogram.types import Message

LOGGER = logging.getLogger(__name__)

def register(app: Client) -> None:
    @app.on_message(filters.group | filters.private, group=-2)
    async def log_all_messages(client: Client, message: Message) -> None:
        user = message.from_user.id if message.from_user else 'unknown'
        chat = message.chat.id if message.chat else 'unknown'
        text = message.text or message.caption or ''
        LOGGER.debug("Received message in %s from %s: %s", chat, user, text)

