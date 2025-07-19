from pyrogram import Client, filters
from utils.decorators import is_admin
from utils.db import add_filter, remove_filter, list_filters, get_filter, clear_filters


@Client.on_message(filters.command('filter') & filters.group)
@is_admin
async def add_filter_cmd(client, message):
    if len(message.command) < 3:
        await message.reply('Usage: /filter <word> <response>')
        return
    keyword = message.command[1].lower()
    response = ' '.join(message.command[2:])
    add_filter(message.chat.id, keyword, response)
    await message.reply(f'Filter "{keyword}" added.')


@Client.on_message(filters.command('stop') & filters.group)
@is_admin
async def stop_filter_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /stop <word>')
        return
    keyword = message.command[1].lower()
    remove_filter(message.chat.id, keyword)
    await message.reply(f'Removed filter "{keyword}".')


@Client.on_message(filters.command('filters') & filters.group)
async def list_filters_cmd(client, message):
    words = list_filters(message.chat.id)
    if not words:
        await message.reply('No filters set.')
    else:
        await message.reply('\n'.join(words))


@Client.on_message(filters.command('stopall') & filters.group)
@is_admin
async def stopall_cmd(client, message):
    clear_filters(message.chat.id)
    await message.reply('All filters cleared.')


@Client.on_message(filters.text & filters.group, group=1)
async def filter_worker(client, message):
    text = message.text.lower()
    for word in list_filters(message.chat.id):
        if word in text:
            response = get_filter(message.chat.id, word)
            if response:
                await message.reply(response)
            break


def register(app):
    pass
