from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from utils.markdown import escape_markdown

async def pinned_cmd(client: Client, message):
    chat = await client.get_chat(message.chat.id)
    if not chat.pinned_message:
        await message.reply('📌 No message is pinned currently.')
    else:
        content = chat.pinned_message.text or chat.pinned_message.caption or '📎 [Media message]'
        await message.reply(f'📌 **Pinned Message:**\n\n{content}', parse_mode='markdown')

@admin_required
async def pin_cmd(client: Client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to pin it.')
        return
    loud = False
    if len(message.command) > 1 and message.command[1].lower() in {'loud', 'notify'}:
        loud = True
    await message.reply_to_message.pin(disable_notification=not loud)
    await message.reply('📌 Message pinned.')

@admin_required
async def permapin_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply('Usage: `/permapin <text>`', parse_mode='markdown')
        return
    text = ' '.join(message.command[1:])
    sent = await message.reply(text)
    await sent.pin()
    await message.reply('📌 Message sent and pinned.')

@admin_required
async def unpin_cmd(client: Client, message):
    if message.reply_to_message:
        await message.reply_to_message.unpin()
        await message.reply('📍 Message unpinned.')
    else:
        await client.unpin_chat_message(message.chat.id)
        await message.reply('📍 Last pinned message removed.')

@admin_required
async def unpin_all_cmd(client: Client, message):
    await client.unpin_all_chat_messages(message.chat.id)
    await message.reply('🧹 All pinned messages have been removed.')

@admin_required
async def antichannelpin_cmd(client: Client, message):
    if len(message.command) == 1:
        state = get_chat_setting(message.chat.id, 'antichannelpin', 'off')
        safe_state = escape_markdown(state)
        await message.reply(f'📡 Anti-channel pin is currently `{safe_state}`.', parse_mode='markdown')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: `/antichannelpin <on/off>`', parse_mode='markdown')
        return
    set_chat_setting(message.chat.id, 'antichannelpin', value)
    safe_val = escape_markdown(value)
    await message.reply(f'📡 Anti-channel pin set to `{safe_val}`.', parse_mode='markdown')

@admin_required
async def cleanlinked_cmd(client: Client, message):
    if len(message.command) == 1:
        state = get_chat_setting(message.chat.id, 'cleanlinked', 'off')
        safe_state = escape_markdown(state)
        await message.reply(f'🧼 Clean linked messages is `{safe_state}`.', parse_mode='markdown')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: `/cleanlinked <on/off>`', parse_mode='markdown')
        return
    set_chat_setting(message.chat.id, 'cleanlinked', value)
    safe_val = escape_markdown(value)
    await message.reply(f'🧼 Clean linked messages set to `{safe_val}`.', parse_mode='markdown')


def register(app):
    app.add_handler(MessageHandler(pinned_cmd, filters.command('pinned', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(pin_cmd, filters.command('pin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(permapin_cmd, filters.command('permapin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(unpin_cmd, filters.command('unpin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(unpin_all_cmd, filters.command('unpinall', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(antichannelpin_cmd, filters.command('antichannelpin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(cleanlinked_cmd, filters.command('cleanlinked', prefixes=PREFIXES) & filters.group), group=0)