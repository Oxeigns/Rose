from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.types import Message, CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import is_admin
from utils.db import set_chat_setting, get_chat_setting
from modules.buttons.admin import admin_panel

@is_admin
async def promote(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to a user to promote them.')
        return
    try:
        await client.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
        await message.reply_text('✅ User has been promoted.')
    except Exception as e:
        await message.reply_text(f'❌ Failed to promote: `{e}`')

@is_admin
async def demote(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to a user to demote them.')
        return
    try:
        await client.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, is_anonymous=False, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
        await message.reply_text('✅ User has been demoted.')
    except Exception as e:
        await message.reply_text(f'❌ Failed to demote: `{e}`')

@is_admin
async def adminlist(client: Client, message: Message):
    try:
        admins = await client.get_chat_members(message.chat.id, filter='administrators')
        text = '**👮 Admin List:**\n'
        async for admin in admins:
            text += f'- {admin.user.mention}\n'
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f'Error fetching admins: `{e}`')

@is_admin
async def admincache(client: Client, message: Message):
    await message.reply_text('🔄 Admin cache has been refreshed.')

@is_admin
async def anonadmin(client: Client, message: Message):
    args = message.command
    if len(args) < 2:
        current = get_chat_setting(message.chat.id, 'anonadmin', 'off')
        await message.reply_text(f'🔒 Anon admin is currently `{current}`.')
        return
    value = args[1].lower()
    if value not in ['on', 'off']:
        await message.reply_text('Usage: `/anonadmin on|off`', parse_mode=ParseMode.MARKDOWN)
        return
    set_chat_setting(message.chat.id, 'anonadmin', value)
    await message.reply_text(f'✅ Anon admin setting updated to `{value}`.')

@is_admin
async def adminerror(client: Client, message: Message):
    args = message.command
    if len(args) < 2:
        current = get_chat_setting(message.chat.id, 'adminerror', 'off')
        await message.reply_text(f'⚠️ Admin errors are currently `{current}`.')
        return
    value = args[1].lower()
    if value not in ['on', 'off']:
        await message.reply_text('Usage: `/adminerror on|off`', parse_mode=ParseMode.MARKDOWN)
        return
    set_chat_setting(message.chat.id, 'adminerror', value)
    await message.reply_text(f'✅ Admin error setting updated to `{value}`.')

@is_admin
async def admin_menu(client: Client, message: Message):
    await message.reply_text('**🛠 Admin Panel**\nChoose what you want to manage:', reply_markup=admin_panel(), parse_mode=ParseMode.MARKDOWN)

async def admin_cb(client: Client, query: CallbackQuery):
    data = query.data.split(':')[1]
    if data == 'promote':
        text = 'Reply with /promote to give admin rights.'
    elif data == 'demote':
        text = 'Reply with /demote to remove admin rights.'
    elif data == 'list':
        text = 'Use /adminlist to see all admins.'
    else:
        text = 'Unknown command.'
    await query.message.edit_text(text, reply_markup=admin_panel(), parse_mode=ParseMode.MARKDOWN)
    await query.answer()


def register(app):
    app.add_handler(MessageHandler(promote, filters.command('promote', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(demote, filters.command('demote', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(adminlist, filters.command('adminlist', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(admincache, filters.command('admincache', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(anonadmin, filters.command('anonadmin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(adminerror, filters.command('adminerror', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(admin_menu, filters.command('admin', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(CallbackQueryHandler(admin_cb, filters.regex('^admin:(?!open$).+')), group=0)
