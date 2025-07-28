import logging
from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from modules.buttons.rules import rules_panel
from pyrogram.errors import RPCError

LOGGER = logging.getLogger(__name__)

async def rules_cmd(client, message):
    cid = message.chat.id if message.chat.type != 'private' else message.from_user.id
    rules = get_chat_setting(cid, 'rules_text', '⚠️ No rules set.')
    button = get_chat_setting(cid, 'rules_button')
    private = get_chat_setting(cid, 'privaterules', 'off') == 'on'

    # If private rules are enabled and command used in group
    if private and message.chat.type != 'private':
        if not message.from_user:
            await message.reply("❌ I can't DM you. Please start me in private first.")
            return
        try:
            await client.send_message(message.from_user.id, rules)
            await message.reply('📩 Rules have been sent to your PM.')
        except RPCError as e:
            LOGGER.warning("Failed to send rules via PM: %s", e)
            await message.reply("❌ I can't DM you. Please start me in private first.")
        return

    markup = (
        InlineKeyboardMarkup([[InlineKeyboardButton(button, callback_data='rules:back')]])
        if button else None
    )
    await message.reply(rules, reply_markup=markup, disable_web_page_preview=True)

@admin_required
async def setrules_cmd(client, message):
    if len(message.command) < 2 and (not message.reply_to_message):
        await message.reply('📝 Usage: `/setrules <text>` or reply to a message', parse_mode='markdown')
        return
    text = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_text', text)
    await message.reply('✅ Rules updated.')

@admin_required
async def private_rules_cmd(client, message):
    current = get_chat_setting(message.chat.id, 'privaterules', 'off')
    new = 'on' if current == 'off' else 'off'
    set_chat_setting(message.chat.id, 'privaterules', new)
    await message.reply(f"📥 Rules will now be sent in {('PM' if new == 'on' else 'chat')}.")

@admin_required
async def reset_rules_cmd(client, message):
    set_chat_setting(message.chat.id, 'rules_text', None)
    await message.reply('🗑️ Rules have been cleared.')

@admin_required
async def set_rules_button(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /setrulesbutton <label>')
        return
    label = ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_button', label)
    await message.reply('✅ Rules button label updated.')

@admin_required
async def reset_rules_button(client, message):
    set_chat_setting(message.chat.id, 'rules_button', None)
    await message.reply('🗑️ Rules button removed.')

async def rules_back(client, query):
    rules = get_chat_setting(query.message.chat.id, 'rules_text', '⚠️ No rules set.')
    await query.message.edit(rules)
    await query.answer()

async def rules_cb(client: Client, query: CallbackQuery):
    data = query.data.split(':')[1]
    if data == 'view':
        text = 'Send /rules to view the current rules.'
    elif data == 'set':
        text = 'Use /setrules or reply with the rules text and /setrules to set it.'
    elif data == 'button':
        text = 'Use /setrulesbutton to set the rules button label.'
    else:
        text = 'Unknown command.'
    await query.message.edit_text(text, reply_markup=rules_panel(), parse_mode='markdown')
    await query.answer()

def register(app):
    app.add_handler(MessageHandler(rules_cmd, filters.command('rules', prefixes=PREFIXES) & (filters.group | filters.private)), group=0)
    app.add_handler(MessageHandler(setrules_cmd, filters.command('setrules', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(private_rules_cmd, filters.command('privaterules', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(reset_rules_cmd, filters.command('resetrules', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(set_rules_button, filters.command('setrulesbutton', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(reset_rules_button, filters.command('resetrulesbutton', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(CallbackQueryHandler(rules_back, filters.regex('^rules:back')), group=0)
    app.add_handler(CallbackQueryHandler(rules_cb, filters.regex('^rules:(?!open$).+')), group=0)
