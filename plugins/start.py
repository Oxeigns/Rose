import logging
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from .help import HELP_MODULES
from utils.errors import catch_errors
from modules.buttons import (
    admin_panel,
    approvals_panel,
    filters_panel,
    lock_panel,
    notes_panel,
    rules_panel,
    warnings_panel,
)
from modules.constants import PREFIXES

LOGGER = logging.getLogger(__name__)

MODULE_BUTTONS = [
    ("⚙️ Admin", "admin:open"),
    ("💬 Filters", "filters:open"),
    ("📜 Rules", "rules:open"),
    ("⚠️ Warnings", "warnings:open"),
    ("✅ Approvals", "approvals:open"),
    ("🔒 Lock", "lock:open"),
    ("📝 Notes", "notes:open"),
]

MODULE_PANELS = {
    "admin": admin_panel,
    "filters": filters_panel,
    "rules": rules_panel,
    "warnings": warnings_panel,
    "approvals": approvals_panel,
    "lock": lock_panel,
    "notes": notes_panel,
}

def build_menu() -> InlineKeyboardMarkup:
    keys, temp = [], []
    for text, cb in MODULE_BUTTONS:
        temp.append(InlineKeyboardButton(text, callback_data=cb))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([InlineKeyboardButton('❌ Close', callback_data='menu:close')])
    return InlineKeyboardMarkup(keys)

def help_menu() -> InlineKeyboardMarkup:
    keys, temp = [], []
    for mod in sorted(HELP_MODULES.keys(), key=str.lower) if HELP_MODULES else []:
        temp.append(InlineKeyboardButton(mod.title(), callback_data=f'help:{mod}'))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([InlineKeyboardButton('❌ Close', callback_data='help:close')])
    return InlineKeyboardMarkup(keys)

@catch_errors
async def start_cmd(client: Client, message: Message):
    LOGGER.debug('📩 /start received')
    chat_type = getattr(message.chat, "type", "")
    from_user_id = getattr(message.from_user, "id", None)
    text = (
        '**Thanks for adding me!**\nUse /menu to configure moderation.'
        if chat_type in ['group', 'supergroup']
        else '**🌹 Rose Bot**\nI help moderate and protect your group.'
    )

    if chat_type == 'private':
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('📋 Menu', callback_data='menu:open')]]
            ),
            quote=True,
            parse_mode="markdown",
        )
    else:
        await message.reply("📩 I've sent you a PM with information.")
        if from_user_id:
            try:
                await client.send_message(
                    from_user_id,
                    text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton('📋 Menu', callback_data='menu:open')]]
                    ),
                    parse_mode="markdown",
                )
            except Exception as e:
                LOGGER.warning("Cannot PM user: %s", e)
                await message.reply("❌ I can't message you. Please start me in PM first.")

@catch_errors
async def menu_cmd(client: Client, message: Message):
    LOGGER.debug('📩 /menu received')
    await message.reply_text(
        '**📋 Control Panel**', reply_markup=build_menu(), quote=True, parse_mode="markdown"
    )

@catch_errors
async def help_cmd(client: Client, message: Message):
    LOGGER.debug('📩 /help received')
    mod = message.command[1].lower() if len(message.command) > 1 else None
    if mod and HELP_MODULES and mod in HELP_MODULES:
        response = HELP_MODULES[mod]
    elif mod:
        response = '❌ Unknown module.\nUse `/help` to see available modules.'
    else:
        response = '**🛠 Help Panel**\nClick a button below to view module commands:'

    chat_type = getattr(message.chat, "type", "")
    from_user_id = getattr(message.from_user, "id", None)

    if chat_type == 'private':
        await message.reply_text(response, reply_markup=help_menu(), parse_mode='markdown')
    else:
        await message.reply("📩 I've sent you a PM with help information.")
        if from_user_id:
            try:
                await client.send_message(
                    from_user_id,
                    response,
                    reply_markup=help_menu(),
                    parse_mode='markdown',
                )
            except Exception as e:
                LOGGER.warning("Cannot PM user: %s", e)
                await message.reply("❌ I can't message you. Please start me in PM first.")

@catch_errors
async def test_cmd(client: Client, message: Message):
    LOGGER.debug('📩 /test received')
    chat_type = getattr(message.chat, "type", "")
    from_user_id = getattr(message.from_user, "id", None)

    if chat_type == 'private':
        await message.reply_text('✅ Test command received!')
    else:
        await message.reply("📩 Check your PM for the test result.")
        if from_user_id:
            try:
                await client.send_message(from_user_id, '✅ Test command received!')
            except Exception as e:
                LOGGER.warning("Cannot PM user: %s", e)
                await message.reply("❌ I can't message you. Please start me in PM first.")

async def menu_open_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 menu:open callback')
    await query.message.edit_text('**📋 Control Panel**', reply_markup=build_menu(), parse_mode='markdown')
    await query.answer()

async def panel_open_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 %s callback', query.data)
    module = query.data.split(':')[0]
    panel_func = MODULE_PANELS.get(module)
    markup = panel_func() if panel_func else InlineKeyboardMarkup(
        [[InlineKeyboardButton('⬅️ Back', callback_data='menu:open')]]
    )
    await query.message.edit_text(f'**🔧 {module.title()} Panel**', reply_markup=markup, parse_mode='markdown')
    await query.answer()

async def menu_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 main:menu callback')
    await query.message.edit_text('**📋 Control Panel**', reply_markup=build_menu(), parse_mode='markdown')
    await query.answer()

async def close_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 menu:close callback')
    await query.message.delete()
    await query.answer()

async def close_main_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 main:close callback')
    await query.message.delete()
    await query.answer()

async def help_cb(client: Client, query: CallbackQuery):
    LOGGER.debug('🟢 %s callback', query.data)
    mod = query.data.split(':')[1]
    if mod == 'close':
        await query.message.delete()
        return
    text = HELP_MODULES.get(mod, '❌ Module not found.')
    await query.message.edit_text(text, reply_markup=help_menu(), parse_mode='markdown')
    await query.answer()

def register(app):
    LOGGER.info("Registering start/menu/help/test handlers...")
    app.add_handler(MessageHandler(start_cmd, filters.command("start", prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(menu_cmd, filters.command("menu", prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(help_cmd, filters.command("help", prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(test_cmd, filters.command("test", prefixes=PREFIXES)), group=0)

    app.add_handler(CallbackQueryHandler(menu_open_cb, filters.regex('^menu:open$')), group=0)
    # Allow lowercase/uppercase/digits before :open
    app.add_handler(CallbackQueryHandler(panel_open_cb, filters.regex('^(?!menu)[A-Za-z0-9_]+:open$')), group=0)
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex('^main:menu$')), group=0)
    app.add_handler(CallbackQueryHandler(close_cb, filters.regex('^menu:close$')), group=0)
    app.add_handler(CallbackQueryHandler(close_main_cb, filters.regex('^main:close$')), group=0)
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex('^help:.+')), group=0)
