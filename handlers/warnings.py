import asyncio
from pyrogram import Client, filters, types
from utils.decorators import is_admin
from utils.db import set_chat_setting, get_chat_setting
from db.warns import add_warn, get_warns, reset_warns, remove_warn


DEFAULT_LIMIT = 3


@Client.on_message(filters.command('warn') & filters.group)
@is_admin
async def warn_user(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to warn.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    reason = ' '.join(message.command[1:]) if len(message.command) > 1 else ''
    count = await add_warn(user_id, chat_id)
    limit = int(get_chat_setting(chat_id, 'warn_limit', DEFAULT_LIMIT))
    await message.reply(f'Warned {message.reply_to_message.from_user.mention}. ({count}/{limit}) {reason}')

    if count >= limit:
        mode = get_chat_setting(chat_id, 'warn_mode', 'ban')
        time_value = int(get_chat_setting(chat_id, 'warn_time', '600'))
        if mode == 'ban':
            await client.ban_chat_member(chat_id, user_id)
            await asyncio.sleep(time_value)
            await client.unban_chat_member(chat_id, user_id)
        elif mode == 'mute':
            await client.restrict_chat_member(chat_id, user_id, permissions=types.ChatPermissions())
            await asyncio.sleep(time_value)
            await client.unrestrict_chat_member(chat_id, user_id)
        await reset_warns(user_id, chat_id)


@Client.on_message(filters.command('warns') & filters.group)
async def warns(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    count = await get_warns(user_id, message.chat.id)
    await message.reply(f'Warns: {count}')


@Client.on_message(filters.command('resetwarn') & filters.group)
@is_admin
async def resetwarn_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to reset warns.')
        return
    await reset_warns(message.reply_to_message.from_user.id, message.chat.id)
    await message.reply('Warns reset.')


@Client.on_message(filters.command(['dwarn', 'rmwarn']) & filters.group)
@is_admin
async def rmwarn_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    count = await remove_warn(user_id, chat_id)
    await message.reply(f'Removed a warn. Remaining: {count}')


@Client.on_message(filters.command('warnlimit') & filters.group)
@is_admin
async def warnlimit(client, message):
    if len(message.command) == 1:
        limit = get_chat_setting(message.chat.id, 'warn_limit', DEFAULT_LIMIT)
        await message.reply(f'Current warn limit: {limit}')
    else:
        try:
            limit = int(message.command[1])
        except ValueError:
            await message.reply('Provide a number for warn limit.')
            return
        set_chat_setting(message.chat.id, 'warn_limit', str(limit))
        await message.reply(f'Warn limit set to {limit}')


@Client.on_message(filters.command('warnmode') & filters.group)
@is_admin
async def warnmode(client, message):
    if len(message.command) == 1:
        mode = get_chat_setting(message.chat.id, 'warn_mode', 'ban')
        await message.reply(f'Current warn mode: {mode}')
    else:
        mode = message.command[1].lower()
        if mode not in {'ban', 'mute'}:
            await message.reply('Modes: ban or mute')
            return
        set_chat_setting(message.chat.id, 'warn_mode', mode)
        await message.reply(f'Warn mode set to {mode}')


@Client.on_message(filters.command('warntime') & filters.group)
@is_admin
async def warntime(client, message):
    if len(message.command) == 1:
        time_value = get_chat_setting(message.chat.id, 'warn_time', '600')
        await message.reply(f'Current warn time: {time_value}s')
    else:
        try:
            sec = int(message.command[1])
        except ValueError:
            await message.reply('Provide time in seconds.')
            return
        set_chat_setting(message.chat.id, 'warn_time', str(sec))
        await message.reply(f'Warn time set to {sec}s')


def register(app):
    pass
