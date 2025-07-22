from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
purge_points = {}

@Client.on_message(filters.command('purge') & filters.group)
@admin_required
async def purge_cmd(client: Client, message):
    if not message.reply_to_message:
        await message.reply('❌ Reply to a message to start purging.')
        return
    limit = None
    if len(message.command) > 1 and message.command[1].isdigit():
        limit = int(message.command[1])
    start_id = message.reply_to_message.id
    end_id = message.id
    ids = list(range(start_id, start_id + limit + 1)) if limit else list(range(start_id, end_id + 1))
    try:
        await client.delete_messages(message.chat.id, ids)
        await message.reply(f'🧹 Deleted `{len(ids)}` messages.', quote=False, parse_mode='markdown')
    except Exception:
        await message.reply('⚠️ Failed to purge messages.')

@Client.on_message(filters.command('spurge') & filters.group)
@admin_required
async def spurge_cmd(client: Client, message):
    if not message.reply_to_message:
        return
    ids = list(range(message.reply_to_message.id, message.id + 1))
    try:
        await client.delete_messages(message.chat.id, ids)
    except Exception:
        pass

@Client.on_message(filters.command('del') & filters.group)
@admin_required
async def del_cmd(client: Client, message):
    if message.reply_to_message:
        try:
            await client.delete_messages(message.chat.id, [message.reply_to_message.id, message.id])
        except Exception:
            pass

@Client.on_message(filters.command('purgefrom') & filters.group)
@admin_required
async def purge_from_cmd(client: Client, message):
    if not message.reply_to_message:
        await message.reply('📍 Reply to a message to mark as purge point.')
        return
    purge_points[message.chat.id] = message.reply_to_message.id
    await message.reply('✅ Purge start point saved.')

@Client.on_message(filters.command('purgeto') & filters.group)
@admin_required
async def purge_to_cmd(client: Client, message):
    start = purge_points.get(message.chat.id)
    if not start:
        await message.reply('⚠️ No purge point set. Use `/purgefrom` first.', parse_mode='markdown')
        return
    ids = list(range(start, message.id + 1))
    try:
        await client.delete_messages(message.chat.id, ids)
        await message.reply(f'🧹 Deleted `{len(ids)}` messages.', quote=False, parse_mode='markdown')
    except Exception:
        await message.reply('⚠️ Failed to purge messages.')
    purge_points.pop(message.chat.id, None)
