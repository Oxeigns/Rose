from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import is_admin
from utils.db import set_chat_setting, get_chat_setting
from buttons.admin import admin_panel

@is_admin
async def promote(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to promote.')
        return
    try:
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        await message.reply('User promoted.')
    except Exception as e:
        await message.reply(f'Failed to promote: {e}')

@is_admin
async def demote(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to demote.')
        return
    try:
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        await message.reply('User demoted.')
    except Exception as e:
        await message.reply(f'Failed to demote: {e}')

@is_admin
async def adminlist(client, message):
    members = await client.get_chat_members(message.chat.id, filter='administrators')
    text = '**Admins:**\n'
    async for m in members:
        text += f'- {m.user.mention}\n'
    await message.reply(text)


@is_admin
async def admincache(client, message):
    await message.reply('Admin cache refreshed.')


@is_admin
async def anonadmin(client, message):
    if len(message.command) < 2:
        state = get_chat_setting(message.chat.id, 'anonadmin', 'off')
        await message.reply(f'Anon admin is currently {state}.')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: /anonadmin on|off')
        return
    set_chat_setting(message.chat.id, 'anonadmin', value)
    await message.reply(f'Anon admin set to {value}.')


@is_admin
async def adminerror(client, message):
    if len(message.command) < 2:
        state = get_chat_setting(message.chat.id, 'adminerror', 'off')
        await message.reply(f'Admin errors are {state}.')
        return
    value = message.command[1].lower()
    if value not in {'on', 'off'}:
        await message.reply('Usage: /adminerror on|off')
        return
    set_chat_setting(message.chat.id, 'adminerror', value)
    await message.reply(f'Admin errors set to {value}.')


@is_admin
async def admin_menu(client, message):
    await message.reply(
        '**\ud83d\udc6e Admin Panel**\nChoose what you want to do:',
        reply_markup=admin_panel(),
    )


def register(app):
    app.add_handler(MessageHandler(promote, filters.command('promote') & filters.group))
    app.add_handler(MessageHandler(demote, filters.command('demote') & filters.group))
    app.add_handler(MessageHandler(adminlist, filters.command('adminlist') & filters.group))
    app.add_handler(MessageHandler(admincache, filters.command('admincache') & filters.group))
    app.add_handler(MessageHandler(anonadmin, filters.command('anonadmin') & filters.group))
    app.add_handler(MessageHandler(adminerror, filters.command('adminerror') & filters.group))
    app.add_handler(MessageHandler(admin_menu, filters.command('admin') & filters.group))
