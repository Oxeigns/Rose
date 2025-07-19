from pyrogram import Client, filters
from utils.decorators import admin_required
from utils.db import get_chat_setting, set_chat_setting
import asyncio


@Client.on_message(filters.command('cleancommand') & filters.group)
@admin_required
async def set_clean(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /cleancommand <seconds|off>')
        return
    arg = message.command[1].lower()
    if arg in {'off', '0'}:
        set_chat_setting(message.chat.id, 'clean_delay', '0')
        await message.reply('Command cleaning disabled.')
    else:
        try:
            delay = int(arg)
        except ValueError:
            await message.reply('Provide a number of seconds or "off".')
            return
        set_chat_setting(message.chat.id, 'clean_delay', str(delay))
        await message.reply(f'Commands will be deleted after {delay} seconds.')


@Client.on_message(filters.command('keepcommand') & filters.group)
@admin_required
async def disable_clean(client, message):
    set_chat_setting(message.chat.id, 'clean_delay', '0')
    await message.reply('Command cleaning disabled.')


# Apply to all messages starting with a command prefix so they can be removed
# after a delay. ``filters.command`` requires specifying commands explicitly,
# so we use a regex filter matching the leading '/' instead.
@Client.on_message(filters.regex(r'^/') & (filters.group | filters.private), group=-1)
async def auto_clean(client, message):
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
