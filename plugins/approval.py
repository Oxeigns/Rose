from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.types import Message, CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from modules.buttons.approvals import approvals_panel
from utils.decorators import admin_required
from utils.db import add_approval, remove_approval, list_approvals, clear_approvals, get_chat_setting, set_chat_setting

@admin_required
async def approve_user(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to a user to approve them.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    await add_approval(chat_id, user_id)
    await message.reply_text(f'✅ Approved [{user_id}](tg://user?id={user_id}).', parse_mode='markdown')

@admin_required
async def unapprove_user(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to a user to unapprove them.')
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    await remove_approval(chat_id, user_id)
    await message.reply_text(f'🚫 Unapproved [{user_id}](tg://user?id={user_id}).', parse_mode='markdown')

@admin_required
async def list_approved(client: Client, message: Message):
    chat_id = message.chat.id
    users = await list_approvals(chat_id)
    if not users:
        await message.reply_text('No users are currently approved.')
        return
    text = '**✅ Approved Users:**\n'
    for user_id in users:
        text += f'- [User](tg://user?id={user_id}) (`{user_id}`)\n'
    await message.reply_text(text, parse_mode='markdown')

@admin_required
async def clear_approved(client: Client, message: Message):
    chat_id = message.chat.id
    await clear_approvals(chat_id)
    await message.reply_text('✅ All approved users have been cleared.')

@admin_required
async def approval_mode_cmd(client: Client, message: Message):
    if len(message.command) == 1:
        current = get_chat_setting(message.chat.id, 'approval_mode', 'off')
        await message.reply_text(f'🔏 Approval mode is `{current}`.', parse_mode='markdown')
        return
    val = message.command[1].lower()
    if val not in {'on', 'off'}:
        await message.reply_text('Usage: `/approvalmode <on/off>`', parse_mode='markdown')
        return
    set_chat_setting(message.chat.id, 'approval_mode', val)
    await message.reply_text(f'🔏 Approval mode set to `{val}`.', parse_mode='markdown')

async def approvals_cb(client: Client, query: CallbackQuery):
    data = query.data.split(':')[1]
    if data == 'approve':
        text = 'Reply with /approve to approve a user.'
    elif data == 'unapprove':
        text = 'Reply with /unapprove to revoke approval.'
    elif data == 'list':
        text = 'Use /approved to list approved users.'
    else:
        text = 'Unknown command.'
    await query.message.edit_text(text, reply_markup=approvals_panel(), parse_mode='markdown')
    await query.answer()


def register(app):
    app.add_handler(MessageHandler(approve_user, filters.command('approve', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(unapprove_user, filters.command('unapprove', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(list_approved, filters.command('approved', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(clear_approved, filters.command('clearapproved', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(approval_mode_cmd, filters.command('approvalmode', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(CallbackQueryHandler(approvals_cb, filters.regex('^approvals:(?!open$).+')), group=0)
