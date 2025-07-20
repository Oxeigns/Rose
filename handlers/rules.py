from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def rules_cmd(client, message):
    rules = get_chat_setting(message.chat.id if message.chat.type != 'private' else message.from_user.id, 'rules_text', 'No rules set.')
    button = get_chat_setting(message.chat.id if message.chat.type != 'private' else message.from_user.id, 'rules_button')
    if get_chat_setting(message.chat.id if message.chat.type != 'private' else message.from_user.id, 'privaterules', 'off') == 'on' and message.chat.type != 'private':
        await client.send_message(message.from_user.id, rules)
        await message.reply('Rules sent in PM.')
        return
    markup = None
    if button:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(button, callback_data='rules:back')]])
    await message.reply(rules, reply_markup=markup, disable_web_page_preview=True)


@admin_required
async def setrules_cmd(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply('Usage: /setrules <text> or reply')
        return
    text = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_text', text)
    await message.reply('Rules updated.')


@admin_required
async def private_rules_cmd(client, message):
    current = get_chat_setting(message.chat.id, 'privaterules', 'off')
    new = 'off' if current == 'on' else 'on'
    set_chat_setting(message.chat.id, 'privaterules', new)
    await message.reply(f'Private rules toggled to {new}.')


@admin_required
async def reset_rules_cmd(client, message):
    set_chat_setting(message.chat.id, 'rules_text', None)
    await message.reply('Rules cleared.')


@admin_required
async def set_rules_button(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /setrulesbutton <name>')
        return
    set_chat_setting(message.chat.id, 'rules_button', ' '.join(message.command[1:]))
    await message.reply('Rules button updated.')


@admin_required
async def reset_rules_button(client, message):
    set_chat_setting(message.chat.id, 'rules_button', None)
    await message.reply('Rules button reset.')


async def rules_back(client, query):
    rules = get_chat_setting(query.message.chat.id, 'rules_text', 'No rules set.')
    await query.message.edit(rules)
    await query.answer()


def register(app: Client):
    app.add_handler(MessageHandler(rules_cmd, filters.command('rules') & (filters.group | filters.private)))
    app.add_handler(MessageHandler(setrules_cmd, filters.command('setrules') & filters.group))
    app.add_handler(MessageHandler(private_rules_cmd, filters.command('privaterules') & filters.group))
    app.add_handler(MessageHandler(reset_rules_cmd, filters.command('resetrules') & filters.group))
    app.add_handler(MessageHandler(set_rules_button, filters.command('setrulesbutton') & filters.group))
    app.add_handler(MessageHandler(reset_rules_button, filters.command('resetrulesbutton') & filters.group))
    app.add_handler(CallbackQueryHandler(rules_back, filters.regex('^rules:back')))
