import asyncio
from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import is_admin
from utils.db import set_chat_setting, get_chat_setting
from db.warns import add_warn, get_warns, reset_warns, remove_warn
import aiosqlite
from db.warns import DB_PATH
from pyrogram.types import CallbackQuery
from buttons.warnings import warnings_panel


DEFAULT_LIMIT = 3

# Warn a user and apply punishments if limit exceeded
@is_admin
async def warn_user(client, message):
    if not message.reply_to_message:
        await message.reply('⚠️ Reply to a user to warn.')
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    reason = ' '.join(message.command[1:]) if len(message.command) > 1 else ''
    count = await add_warn(user_id, chat_id)
    limit = int(get_chat_setting(chat_id, 'warn_limit', DEFAULT_LIMIT))

    await message.reply(f'⚠️ Warned {message.reply_to_message.from_user.mention} ({count}/{limit})\n{reason}')

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


# Delete and warn
@is_admin
async def dwarn_user(client, message):
    if message.reply_to_message:
        await message.reply_to_message.delete()
        await warn_user(client, message)

# Silent warn without replies
@is_admin
async def swarn_user(client, message):
    if message.reply_to_message:
        await message.reply_to_message.delete()
        await warn_user(client, message)

# Warn with silent PM notice
@is_admin
async def soft_warn(client, message):
    if not message.reply_to_message:
        await message.reply('⚠️ Reply to a user to warn.')
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    reason = ' '.join(message.command[1:]) if len(message.command) > 1 else ''
    count = await add_warn(user_id, chat_id)
    limit = int(get_chat_setting(chat_id, 'warn_limit', DEFAULT_LIMIT))

    try:
        await message.reply_to_message.reply(f'You were warned in {message.chat.title}. ({count}/{limit}) {reason}')
    except:
        pass

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


# Show current warns
async def warns(client, message):
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    count = await get_warns(user_id, message.chat.id)
    await message.reply(f"⚠️ Current warns: {count}")

# Reset warns for a user
@is_admin
async def resetwarn_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('⚠️ Reply to a user to reset warns.')
        return
    await reset_warns(message.reply_to_message.from_user.id, message.chat.id)
    await message.reply('✅ Warns reset.')

# Remove one warn
@is_admin
async def rmwarn_cmd(client, message):
    if not message.reply_to_message:
        await message.reply('⚠️ Reply to a user.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    count = await remove_warn(user_id, chat_id)
    await message.reply(f"✅ Removed one warn. Remaining: {count}")

# Reset all warns in chat
@is_admin
async def reset_all_warns(client, message):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM warns WHERE chat_id=?", (message.chat.id,))
        await db.commit()
    await message.reply("🧹 All warns reset for this chat.")

# Show settings
async def warnings_settings(client, message):
    limit = get_chat_setting(message.chat.id, 'warn_limit', DEFAULT_LIMIT)
    mode = get_chat_setting(message.chat.id, 'warn_mode', 'ban')
    time_value = get_chat_setting(message.chat.id, 'warn_time', '600')
    await message.reply(f"**Warn Settings:**\nLimit: {limit}\nMode: {mode}\nDuration: {time_value}s")

# Set warn limit
@is_admin
async def warnlimit(client, message):
    if len(message.command) == 1:
        current = get_chat_setting(message.chat.id, 'warn_limit', DEFAULT_LIMIT)
        await message.reply(f"📛 Current warn limit: {current}")
        return
    try:
        limit = int(message.command[1])
        set_chat_setting(message.chat.id, 'warn_limit', str(limit))
        await message.reply(f"✅ Warn limit set to {limit}")
    except ValueError:
        await message.reply("❗ Enter a valid number.")

# Set warn punishment mode
@is_admin
async def warnmode(client, message):
    if len(message.command) == 1:
        mode = get_chat_setting(message.chat.id, 'warn_mode', 'ban')
        await message.reply(f"🚦 Current warn mode: {mode}")
        return
    mode = message.command[1].lower()
    if mode not in {'ban', 'mute'}:
        await message.reply("❗ Invalid mode. Use `ban` or `mute`.")
        return
    set_chat_setting(message.chat.id, 'warn_mode', mode)
    await message.reply(f"✅ Warn mode set to {mode}")

# Set mute/ban duration
@is_admin
async def warntime(client, message):
    if len(message.command) == 1:
        current = get_chat_setting(message.chat.id, 'warn_time', '600')
        await message.reply(f"⏱️ Warn punishment time: {current}s")
        return
    try:
        seconds = int(message.command[1])
        set_chat_setting(message.chat.id, 'warn_time', str(seconds))
        await message.reply(f"✅ Warn time set to {seconds}s")
    except ValueError:
        await message.reply("❗ Enter duration in seconds.")

# Callback buttons from warnings panel
async def warnings_cb(client: Client, query: CallbackQuery):
    data = query.data.split(":")[1]
    if data == "warn":
        text = "Reply with /warn to warn a user."
    elif data == "limit":
        text = "Use /warnlimit <num> to set warn limit."
    elif data == "settings":
        text = "Use /warnings to view current settings."
    else:
        text = "Unknown command."
    await query.message.edit_text(text, reply_markup=warnings_panel(), parse_mode="markdown")
    await query.answer()

# Register all handlers
def register(app):
    app.add_handler(MessageHandler(warn_user, filters.command('warn') & filters.group))
    app.add_handler(MessageHandler(dwarn_user, filters.command('dwarn') & filters.group))
    app.add_handler(MessageHandler(swarn_user, filters.command('swarn') & filters.group))
    app.add_handler(MessageHandler(soft_warn, filters.command('softwarn') & filters.group))
    app.add_handler(MessageHandler(warns, filters.command('warns') & filters.group))
    app.add_handler(MessageHandler(resetwarn_cmd, filters.command('resetwarn') & filters.group))
    app.add_handler(MessageHandler(rmwarn_cmd, filters.command('rmwarn') & filters.group))
    app.add_handler(MessageHandler(reset_all_warns, filters.command('resetallwarns') & filters.group))
    app.add_handler(MessageHandler(warnlimit, filters.command('warnlimit') & filters.group))
    app.add_handler(MessageHandler(warnmode, filters.command('warnmode') & filters.group))
    app.add_handler(MessageHandler(warntime, filters.command('warntime') & filters.group))
    app.add_handler(MessageHandler(warnings_settings, filters.command('warnings') & filters.group))
    app.add_handler(CallbackQueryHandler(warnings_cb, filters.regex(r'^warnings:(?!open$).+')))
