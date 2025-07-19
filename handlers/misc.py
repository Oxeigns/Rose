from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MODULE_BUTTONS = [
    ('Admin \u2699\ufe0f', 'admin:open'),
    ('Filters \ud83d\udcac', 'filters:open'),
    ('Rules \ud83d\udcdc', 'rules:open'),
    ('Warnings \u26a0\ufe0f', 'warnings:open'),
    ('Approvals \u2705', 'approvals:open'),
    ('Lock \ud83d\udd12', 'lock:open'),
]

async def start(client, message):
    await message.reply(
        '**Rose Bot**\nUse /menu to view modules.',
        quote=True
    )

async def menu(client, message):
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in MODULE_BUTTONS]
    )
    await message.reply(
        '**Control Panel**',
        reply_markup=markup,
        quote=True
    )

async def panel_open(client, query):
    module = query.data.split(':', 1)[0]
    await query.message.edit(
        f'**{module.title()} Panel**',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back \u2b05\ufe0f', callback_data='main:menu')]])
    )
    await query.answer()

async def menu_cb(client, query):
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in MODULE_BUTTONS]
    )
    await query.message.edit('**Control Panel**', reply_markup=markup)
    await query.answer()


def register(app):
    app.add_handler(MessageHandler(start, filters.command('start')))
    app.add_handler(MessageHandler(menu, filters.command('menu')))
    app.add_handler(CallbackQueryHandler(panel_open, filters.regex('^[a-z]+:open$')))
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex('^main:menu$')))
