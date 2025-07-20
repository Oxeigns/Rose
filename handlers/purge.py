from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required

purge_points = {}


@admin_required
async def purge_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to start purging.')
        return
    limit = None
    if len(message.command) > 1 and message.command[1].isdigit():
        limit = int(message.command[1])
    ids = []
    start_id = message.reply_to_message.id
    if limit:
        ids = list(range(start_id, start_id + limit + 1))
    else:
        ids = list(range(start_id, message.id + 1))
    await client.delete_messages(message.chat.id, ids)
    await message.reply(f'Deleted {len(ids)} messages.', quote=False)


@admin_required
async def spurge_cmd(client, message):
    if not message.reply_to_message:
        return
    ids = list(range(message.reply_to_message.id, message.id + 1))
    await client.delete_messages(message.chat.id, ids)


@admin_required
async def del_cmd(client, message):
    if message.reply_to_message:
        await client.delete_messages(message.chat.id, [message.reply_to_message.id, message.id])


@admin_required
async def purge_from_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to set purge point.')
        return
    purge_points[message.chat.id] = message.reply_to_message.id
    await message.reply('Purge from point saved.')


@admin_required
async def purge_to_cmd(client, message):
    start = purge_points.get(message.chat.id)
    if not start:
        await message.reply('No purgefrom point set.')
        return
    ids = list(range(start, message.id + 1))
    await client.delete_messages(message.chat.id, ids)
    purge_points.pop(message.chat.id, None)
    await message.reply(f'Deleted {len(ids)} messages.', quote=False)


def register(app: Client):
    app.add_handler(MessageHandler(purge_cmd, filters.command('purge') & filters.group))
    app.add_handler(MessageHandler(spurge_cmd, filters.command('spurge') & filters.group))
    app.add_handler(MessageHandler(del_cmd, filters.command('del') & filters.group))
    app.add_handler(MessageHandler(purge_from_cmd, filters.command('purgefrom') & filters.group))
    app.add_handler(MessageHandler(purge_to_cmd, filters.command('purgeto') & filters.group))
