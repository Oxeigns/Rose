from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# /rules - shows rules in group or PM
async def rules_cmd(client, message):
    cid = message.chat.id if message.chat.type != 'private' else message.from_user.id
    rules = get_chat_setting(cid, 'rules_text', '⚠️ No rules set.')
    button = get_chat_setting(cid, 'rules_button')
    private = get_chat_setting(cid, 'privaterules', 'off') == 'on'

    if private and message.chat.type != 'private':
        try:
            await client.send_message(message.from_user.id, rules)
            await message.reply("📩 Rules have been sent to your PM.")
        except:
            await message.reply("❌ I can't DM you. Please start me in private first.")
        return

    markup = InlineKeyboardMarkup([[InlineKeyboardButton(button, callback_data="rules:back")]]) if button else None
    await message.reply(rules, reply_markup=markup, disable_web_page_preview=True)


# /setrules <text> or reply
@admin_required
async def setrules_cmd(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("📝 Usage: `/setrules <text>` or reply to a message", parse_mode="markdown")
        return
    text = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_text', text)
    await message.reply("✅ Rules updated.")


# /privaterules toggle
@admin_required
async def private_rules_cmd(client, message):
    current = get_chat_setting(message.chat.id, 'privaterules', 'off')
    new = 'on' if current == 'off' else 'off'
    set_chat_setting(message.chat.id, 'privaterules', new)
    await message.reply(f"📥 Rules will now be sent in {'PM' if new == 'on' else 'chat'}.")


# /resetrules
@admin_required
async def reset_rules_cmd(client, message):
    set_chat_setting(message.chat.id, 'rules_text', None)
    await message.reply("🗑️ Rules have been cleared.")


# /setrulesbutton <label>
@admin_required
async def set_rules_button(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /setrulesbutton <label>")
        return
    label = ' '.join(message.command[1:])
    set_chat_setting(message.chat.id, 'rules_button', label)
    await message.reply("✅ Rules button label updated.")


# /resetrulesbutton
@admin_required
async def reset_rules_button(client, message):
    set_chat_setting(message.chat.id, 'rules_button', None)
    await message.reply("🗑️ Rules button removed.")


# Callback when rules button is clicked
async def rules_back(client, query):
    rules = get_chat_setting(query.message.chat.id, 'rules_text', '⚠️ No rules set.')
    await query.message.edit(rules)
    await query.answer()


# Register handlers
def register(app: Client):
    app.add_handler(MessageHandler(rules_cmd, filters.command('rules') & (filters.group | filters.private)))
    app.add_handler(MessageHandler(setrules_cmd, filters.command('setrules') & filters.group))
    app.add_handler(MessageHandler(private_rules_cmd, filters.command('privaterules') & filters.group))
    app.add_handler(MessageHandler(reset_rules_cmd, filters.command('resetrules') & filters.group))
    app.add_handler(MessageHandler(set_rules_button, filters.command('setrulesbutton') & filters.group))
    app.add_handler(MessageHandler(reset_rules_button, filters.command('resetrulesbutton') & filters.group))
    app.add_handler(CallbackQueryHandler(rules_back, filters.regex('^rules:back')))
