from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MODULES = [
    'Admin', 'Antiflood', 'Captcha', 'Notes', 'Warnings'
]

@Client.on_message(filters.command('start'))
async def start(client, message):
    await message.reply(
        '**Rose Bot**\nUse /menu to view modules.',
        quote=True
    )

@Client.on_message(filters.command('menu'))
async def menu(client, message):
    buttons = [[InlineKeyboardButton(m, callback_data=f'help:{m}')]
               for m in MODULES]
    await message.reply(
        '**\ud83d\udcda Available Modules**',
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )

@Client.on_callback_query(filters.regex('^help:'))
async def help_cb(client, query):
    module = query.data.split(':', 1)[1]
    await query.message.edit(f'**{module} Module**\nWork in progress.',
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back \u2b05\ufe0f', callback_data='menu')]]))
    await query.answer()

@Client.on_callback_query(filters.regex('^menu$'))
async def menu_cb(client, query):
    buttons = [[InlineKeyboardButton(m, callback_data=f'help:{m}')]
               for m in MODULES]
    await query.message.edit(
        '**\ud83d\udcda Available Modules**',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await query.answer()
