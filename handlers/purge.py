from pyrogram import Client, filters
from utils.decorators import admin_required

purge_points = {}


@Client.on_message(filters.command('purge') & filters.group)
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


@Client.on_message(filters.command('spurge') & filters.group)
@admin_required
async def spurge_cmd(client, message):
    if not message.reply_to_message:
        return
    ids = list(range(message.reply_to_message.id, message.id + 1))
    await client.delete_messages(message.chat.id, ids)


@Client.on_message(filters.command('del') & filters.group)
@admin_required
async def del_cmd(client, message):
    if message.reply_to_message:
        await client.delete_messages(message.chat.id, [message.reply_to_message.id, message.id])


@Client.on_message(filters.command('purgefrom') & filters.group)
@admin_required
async def purge_from_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a message to set purge point.')
        return
    purge_points[message.chat.id] = message.reply_to_message.id
    await message.reply('Purge from point saved.')


@Client.on_message(filters.command('purgeto') & filters.group)
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
    pass
