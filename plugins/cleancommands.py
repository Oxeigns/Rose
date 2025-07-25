from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import get_chat_setting, set_chat_setting
import asyncio

@admin_required
async def set_clean(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/cleancommand <seconds|off>`', parse_mode='markdown')
        return
    arg = message.command[1].lower()
    if arg in {'off', '0'}:
        set_chat_setting(message.chat.id, 'clean_delay', '0')
        await message.reply_text('🧹 Command auto-cleaning is now *disabled*.')
    else:
        try:
            delay = int(arg)
            if delay < 1:
                raise ValueError
        except ValueError:
            await message.reply_text('Please provide a number greater than 0 or use `off`.', parse_mode='markdown')
            return
        set_chat_setting(message.chat.id, 'clean_delay', str(delay))
        await message.reply_text(f'🧼 Commands will be deleted after `{delay}` seconds.', parse_mode='markdown')

@admin_required
async def keep_command(client: Client, message: Message):
    set_chat_setting(message.chat.id, 'clean_delay', '0')
    await message.reply_text('✅ Command cleaning has been *turned off*.')

async def auto_clean(client: Client, message: Message):
    delay = get_chat_setting(message.chat.id, 'clean_delay', '0')
    try:
        delay_int = int(delay)
    except (TypeError, ValueError):
        return
    if delay_int > 0:
        await asyncio.sleep(delay_int)
        try:
            await message.delete()
        except Exception:
            pass


def register(app):
    app.add_handler(MessageHandler(set_clean, filters.command('cleancommand', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(keep_command, filters.command('keepcommand', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(auto_clean, filters.regex('^/') & (filters.group | filters.private)), group=-1)