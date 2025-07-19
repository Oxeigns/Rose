from pyrogram import Client, filters
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting


@Client.on_message(filters.command('pinned') & filters.group)
async def pinned_cmd(client, message):
    chat = await client.get_chat(message.chat.id)
    if not chat.pinned_message:
        await message.reply('No pinned message.')
    else:
        await message.reply(chat.pinned_message.text or 'Pinned message.')


@Client.on_message(filters.command('pin') & filters.group)
@admin_required
async def pin_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to pin.')
        return
    loud = False
    if len(message.command) > 1 and message.command[1].lower() in {'loud', 'notify'}:
        loud = True
    await message.reply_to_message.pin(disable_notification=not loud)


@Client.on_message(filters.command('permapin') & filters.group)
@admin_required
async def permapin_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /permapin <text>')
        return
    sent = await message.reply(' '.join(message.command[1:]))
    await sent.pin()


@Client.on_message(filters.command('unpin') & filters.group)
@admin_required
async def unpin_cmd(client, message):
    if message.reply_to_message:
        await message.reply_to_message.unpin()
    else:
        await client.unpin_chat_message(message.chat.id)


@Client.on_message(filters.command('unpinall') & filters.group)
@admin_required
async def unpin_all_cmd(client, message):
    await client.unpin_all_chat_messages(message.chat.id)


@Client.on_message(filters.command('antichannelpin') & filters.group)
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


@Client.on_message(filters.command('cleanlinked') & filters.group)
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
    pass
