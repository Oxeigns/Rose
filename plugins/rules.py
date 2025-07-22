from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from modules.buttons.rules import rules_panel

@Client.on_message(filters.command('rules') & (filters.group | filters.private))
async def rules_cmd(client, message):
    cid = message.chat.id if message.chat.type != 'private' else message.from_user.id
    rules = get_chat_setting(cid, 'rules_text', '⚠️ No rules set.')
    button = get_chat_setting(cid, 'rules_button')
    private = get_chat_setting(cid, 'privaterules', 'off') == 'on'
    if private and message.chat.type != 'private':
        try:
            await client.send_message(message.from_user.id, rules)
            await message.reply('📩 Rules have been sent to your PM.')
        except:
            await message.reply("❌ I can't DM you. Please start me in private first.")
        return
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(button, callback_data='rules:back')]]) if button else None
    await message.reply(rules, reply_markup=markup, disable_web_page_preview=True)

@Client.on_message(filters.command('setrules') & filters.group)
@admin_required
async def setrules_cmd(client, message):
    if len(message.command) < 2 and (not message.reply_to_message):
        await message.reply('📝 Usage: `/setrules <text>` or reply to a message', parse_mode='markdown')
        return
    text = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_text', text)
    await message.reply('✅ Rules updated.')

@Client.on_message(filters.command('privaterules') & filters.group)
@admin_required
async def private_rules_cmd(client, message):
    current = get_chat_setting(message.chat.id, 'privaterules', 'off')
    new = 'on' if current == 'off' else 'off'
    set_chat_setting(message.chat.id, 'privaterules', new)
    await message.reply(f"📥 Rules will now be sent in {('PM' if new == 'on' else 'chat')}.")

@Client.on_message(filters.command('resetrules') & filters.group)
@admin_required
async def reset_rules_cmd(client, message):
    set_chat_setting(message.chat.id, 'rules_text', None)
    await message.reply('🗑️ Rules have been cleared.')

@Client.on_message(filters.command('setrulesbutton') & filters.group)
@admin_required
async def set_rules_button(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /setrulesbutton <label>')
        return
    label = ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_button', label)
    await message.reply('✅ Rules button label updated.')

@Client.on_message(filters.command('resetrulesbutton') & filters.group)
@admin_required
async def reset_rules_button(client, message):
    set_chat_setting(message.chat.id, 'rules_button', None)
    await message.reply('🗑️ Rules button removed.')

@Client.on_callback_query(filters.regex('^rules:back'))
async def rules_back(client, query):
    rules = get_chat_setting(query.message.chat.id, 'rules_text', '⚠️ No rules set.')
    await query.message.edit(rules)
    await query.answer()

@Client.on_callback_query(filters.regex('^rules:(?!open$).+'))
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
