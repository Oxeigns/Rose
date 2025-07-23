import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

LOGGER = logging.getLogger(__name__)
LOGGER.info("🔧 Debug plugin loaded")


async def log_all_messages(client: Client, message: Message) -> None:
    user = message.from_user
    chat = message.chat
    chat_title = chat.title if chat and chat.title else "Private"
    msg_type = "Group" if chat and chat.type in ("group", "supergroup") else "Private"
    text = message.text or message.caption or ""
    LOGGER.debug(
        "[%s] %s (%s) in %s (%s): %s",
        msg_type,
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat_title,
        chat.id if chat else "N/A",
        text.replace("\n", " "),
    )


async def log_queries(client: Client, query: CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat if query.message else None
    chat_title = chat.title if chat and chat.title else "Private"
    msg_type = "Group" if chat and chat.type in ("group", "supergroup") else "Private"
    LOGGER.debug(
        "[Callback %s] %s (%s) in %s (%s): %s",
        msg_type,
        user.first_name if user else "Unknown",
        user.id if user else "N/A",
        chat_title,
        chat.id if chat else "N/A",
        query.data,
    )


async def debug_catch_all(client: Client, message: Message) -> None:
    """Log any received message to confirm update reception."""
    LOGGER.debug(
        "[DEBUG] Catch-all message from %s (%s) in %s (%s)",
        message.from_user.first_name if message.from_user else "Unknown",
        message.from_user.id if message.from_user else "N/A",
        message.chat.title if message.chat else "Private",
        message.chat.id if message.chat else "N/A",
    )


def register(app):
    app.add_handler(MessageHandler(log_all_messages, filters.group | filters.private), group=-2)
    app.add_handler(CallbackQueryHandler(log_queries), group=-2)
    app.add_handler(MessageHandler(debug_catch_all, filters.all), group=-1)
