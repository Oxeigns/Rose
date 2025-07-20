from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting


async def pinned_cmd(client, message):
    chat = await client.get_chat(message.chat.id)
    if not chat.pinned_message:
        await message.reply('No pinned message.')
    else:
        await message.reply(chat.pinned_message.text or 'Pinned message.')


@admin_required
async def pin_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to pin.')
        return
    loud = False
    if len(message.command) > 1 and message.command[1].lower() in {'loud', 'notify'}:
        loud = True
    await message.reply_to_message.pin(disable_notification=not loud)


@admin_required
async def permapin_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /permapin <text>')
        return
    sent = await message.reply(' '.join(message.command[1:]))
    await sent.pin()


@admin_required
async def unpin_cmd(client, message):
    if message.reply_to_message:
        await message.reply_to_message.unpin()
    else:
        await client.unpin_chat_message(message.chat.id)


@admin_required
async def unpin_all_cmd(client, message):
    await client.unpin_all_chat_messages(message.chat.id)


@admin_required
async def antichannelpin_cmd(client, message):
    if len(message.command) == 1:
        state = get_chat_setting(message.chat.id, 'antichannelpin', 'off')
        await message.reply(f'Anti-channel pin is {state}.')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: /antichannelpin <on/off>')
        return
    set_chat_setting(message.chat.id, 'antichannelpin', value)
    await message.reply(f'Anti-channel pin set to {value}.')


@admin_required
async def cleanlinked_cmd(client, message):
    if len(message.command) == 1:
        state = get_chat_setting(message.chat.id, 'cleanlinked', 'off')
        await message.reply(f'Clean linked messages is {state}.')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: /cleanlinked <on/off>')
        return
    set_chat_setting(message.chat.id, 'cleanlinked', value)
    await message.reply(f'Clean linked messages set to {value}.')


def register(app: Client):
    app.add_handler(MessageHandler(pinned_cmd, filters.command('pinned') & filters.group))
    app.add_handler(MessageHandler(pin_cmd, filters.command('pin') & filters.group))
    app.add_handler(MessageHandler(permapin_cmd, filters.command('permapin') & filters.group))
    app.add_handler(MessageHandler(unpin_cmd, filters.command('unpin') & filters.group))
    app.add_handler(MessageHandler(unpin_all_cmd, filters.command('unpinall') & filters.group))
    app.add_handler(MessageHandler(antichannelpin_cmd, filters.command('antichannelpin') & filters.group))
    app.add_handler(MessageHandler(cleanlinked_cmd, filters.command('cleanlinked') & filters.group))
