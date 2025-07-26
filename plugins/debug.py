import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.handlers import CallbackQueryHandler

LOGGER = logging.getLogger(__name__)
LOGGER.info("🔧 Debug plugin loaded")


async def log_all_messages(client: Client, message: Message) -> None:
    user = message.from_user.id if message.from_user else "N/A"
    chat = message.chat.id if message.chat else "PM"
    text = message.text or message.caption or ""
    print(f"[DBG] {user} in {chat}: {text.replace('\n', ' ')}")


async def log_queries(client: Client, query: CallbackQuery) -> None:
    user = query.from_user.id if query.from_user else "N/A"
    chat = query.message.chat.id if query.message else "PM"
    print(f"[CB] {user} in {chat}: {query.data}")


async def debug_catch_all(client: Client, message: Message) -> None:
    """Log any received message to confirm update reception."""
    user = message.from_user.id if message.from_user else "N/A"
    chat = message.chat.id if message.chat else "PM"
    print(f"[DBG-ALL] {user} in {chat}")


def register(app):
    # Only register the callback query logger to avoid duplicate message handlers
    app.add_handler(CallbackQueryHandler(log_queries), group=-2)
