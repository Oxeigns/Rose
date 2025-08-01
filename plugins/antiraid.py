from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
import time
ANTIRAID_STATUS = {}
JOINS_TIMESTAMPS = {}
COOLDOWN_DURATION = 30

@admin_required
async def toggle_antiraid(client: Client, message: Message):
    args = message.command
    if len(args) == 1:
        current = ANTIRAID_STATUS.get(message.chat.id, 'off')
        await message.reply_text(f'🚨 Antiraid is currently `{current}`.')
        return
    status = args[1].lower()
    if status not in ['on', 'off']:
        await message.reply_text('Usage: `/antiraid on|off`', parse_mode=ParseMode.MARKDOWN)
        return
    ANTIRAID_STATUS[message.chat.id] = status
    await message.reply_text(f'✅ Antiraid mode set to `{status}`.')

async def new_member_joined(client: Client, message: Message):
    chat_id = message.chat.id
    status = ANTIRAID_STATUS.get(chat_id, 'off')
    if status != 'on':
        return
    for user in message.new_chat_members:
        if user.is_bot:
            continue
        JOINS_TIMESTAMPS[chat_id, user.id] = time.time()

async def restrict_new_user(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    if not user_id or ANTIRAID_STATUS.get(chat_id) != 'on':
        return
    join_time = JOINS_TIMESTAMPS.get((chat_id, user_id))
    if not join_time:
        return
    if time.time() - join_time < COOLDOWN_DURATION:
        try:
            await message.delete()
        except Exception:
            pass


def register(app):
    app.add_handler(MessageHandler(toggle_antiraid, filters.command('antiraid', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(new_member_joined, filters.new_chat_members), group=0)
    app.add_handler(MessageHandler(restrict_new_user, filters.group & filters.text & ~filters.service), group=0)
