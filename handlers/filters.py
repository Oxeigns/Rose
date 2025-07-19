from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import is_admin
from utils.db import add_filter, remove_filter, list_filters, get_filter, clear_filters


@is_admin
async def add_filter_cmd(client, message):
    if len(message.command) < 3:
        await message.reply('Usage: /filter <word> <response>')
        return
    keyword = message.command[1].lower()
    response = ' '.join(message.command[2:])
    add_filter(message.chat.id, keyword, response)
    await message.reply(f'Filter "{keyword}" added.')


@is_admin
async def stop_filter_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /stop <word>')
        return
    keyword = message.command[1].lower()
    remove_filter(message.chat.id, keyword)
    await message.reply(f'Removed filter "{keyword}".')


async def list_filters_cmd(client, message):
    words = list_filters(message.chat.id)
    if not words:
        await message.reply('No filters set.')
    else:
        await message.reply('\n'.join(words))


@is_admin
async def stopall_cmd(client, message):
    clear_filters(message.chat.id)
    await message.reply('All filters cleared.')


async def filter_worker(client, message):
    text = message.text.lower()
    for word in list_filters(message.chat.id):
        if word in text:
            response = get_filter(message.chat.id, word)
            if response:
                await message.reply(response)
            break


def register(app):
    app.add_handler(MessageHandler(add_filter_cmd, filters.command('filter') & filters.group))
    app.add_handler(MessageHandler(stop_filter_cmd, filters.command('stop') & filters.group))
    app.add_handler(MessageHandler(list_filters_cmd, filters.command('filters') & filters.group))
    app.add_handler(MessageHandler(stopall_cmd, filters.command('stopall') & filters.group))
    app.add_handler(MessageHandler(filter_worker, filters.text & filters.group), group=1)
