import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

LOGGER = logging.getLogger(__name__)

@Client.on_message(filters.group | filters.private, group=-2)
async def log_all_messages(client: Client, message: Message) -> None:
    user = message.from_user
    chat = message.chat
    chat_title = chat.title if chat and chat.title else 'Private'
    msg_type = 'Group' if chat and chat.type in ('group', 'supergroup') else 'Private'
    text = message.text or message.caption or ''
    LOGGER.debug('[%s] %s (%s) in %s (%s): %s', msg_type, user.first_name if user else 'Unknown', user.id if user else 'N/A', chat_title, chat.id if chat else 'N/A', text.replace('\n', ' '))

@Client.on_callback_query(group=-2)
async def log_queries(client: Client, query: CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat if query.message else None
    chat_title = chat.title if chat and chat.title else 'Private'
    msg_type = 'Group' if chat and chat.type in ('group', 'supergroup') else 'Private'
    LOGGER.debug('[Callback %s] %s (%s) in %s (%s): %s', msg_type, user.first_name if user else 'Unknown', user.id if user else 'N/A', chat_title, chat.id if chat else 'N/A', query.data)
