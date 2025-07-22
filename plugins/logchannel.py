from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from utils.markdown import escape_markdown

@Client.on_message(filters.command('logchannel') & filters.group)
@admin_required
async def logchannel_handler(client: Client, message: Message):
    if len(message.command) == 1:
        log_id = get_chat_setting(message.chat.id, 'log_channel')
        if log_id:
            safe_id = escape_markdown(str(log_id))
            await message.reply_text(f'📝 Log channel is set to: `{safe_id}`', parse_mode='markdown')
        else:
            await message.reply_text('ℹ️ No log channel set.')
        return
    arg = message.command[1].lower()
    if arg == 'off':
        set_chat_setting(message.chat.id, 'log_channel', None)
        await message.reply_text('🚫 Logging disabled.')
        return
    try:
        target = message.command[1]
        if target.startswith('@'):
            chat = await client.get_chat(target)
        else:
            chat = await client.get_chat(int(target))
        if not chat.type in ('channel', 'supergroup'):
            await message.reply_text('❌ Not a valid channel or supergroup.')
            return
        member = await client.get_chat_member(chat.id, client.me.id)
        if not member.can_post_messages:
            await message.reply_text('❌ Bot must be an admin in that channel to post logs.')
            return
        set_chat_setting(message.chat.id, 'log_channel', chat.id)
        safe_title = escape_markdown(chat.title)
        await message.reply_text(f'✅ Logs will be sent to: `{safe_title}` (`{chat.id}`)', parse_mode='markdown')
    except Exception as e:
        safe_err = escape_markdown(str(e))
        await message.reply_text(f'❌ Failed to set log channel:\n`{safe_err}`', parse_mode='markdown')

async def send_log(client: Client, chat_id: int, text: str):
    log_id = get_chat_setting(chat_id, 'log_channel')
    if not log_id:
        return
    try:
        await client.send_message(log_id, text, parse_mode='markdown')
    except Exception:
        pass
