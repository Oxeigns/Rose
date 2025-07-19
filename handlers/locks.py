from pyrogram import Client, filters, types
from utils.decorators import admin_required

LOCK_MAP = {
    'sticker': 'can_send_stickers',
    'media': 'can_send_media_messages',
    'photo': 'can_send_photos',
    'video': 'can_send_videos',
}


@Client.on_message(filters.command('lock') & filters.group)
@admin_required
async def lock_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /lock <type>')
        return
    lock_type = message.command[1].lower()
    perm = LOCK_MAP.get(lock_type)
    if not perm:
        await message.reply('Unknown lock type.')
        return
    perms = types.ChatPermissions(**{perm: False})
    await client.set_chat_permissions(message.chat.id, perms)
    await message.reply(f'Locked {lock_type}.')


@Client.on_message(filters.command('unlock') & filters.group)
@admin_required
async def unlock_cmd(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /unlock <type>')
        return
    lock_type = message.command[1].lower()
    perm = LOCK_MAP.get(lock_type)
    if not perm:
        await message.reply('Unknown lock type.')
        return
    perms = types.ChatPermissions(**{perm: True})
    await client.set_chat_permissions(message.chat.id, perms)
    await message.reply(f'Unlocked {lock_type}.')


def register(app: Client):
    pass
