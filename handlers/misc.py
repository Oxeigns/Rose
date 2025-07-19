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


RUN_STRINGS = [
    "Eeny meeny miny moe...",
    "Time to run away!",
    "Let's hide!",
    "Runs to the hills!",
]

async def runs(client, message):
    await message.reply(random.choice(RUN_STRINGS))

async def get_id(client, message):
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    if message.command and len(message.command) > 1:
        username = message.command[1].lstrip('@')
        try:
            target = await client.get_users(username)
        except Exception:
            pass
    await message.reply(f'`{target.id}`')

async def info(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    text = f"**{user.first_name}**\nID: `{user.id}`"
    if user.username:
        text += f"\n@{user.username}"
    if user.bio:
        text += f"\n{user.bio}"
    await message.reply(text)

async def donate(client, message):
    await message.reply("[Donate here](https://example.com/donate)", disable_web_page_preview=True)

async def markdown_help(client, message):
    if message.chat.type != 'private':
        await message.reply('I\'ve messaged you the Markdown guide!')
    await client.send_message(message.from_user.id, '**Markdown Guide**\nUse `*bold*`, `_italic_`, `[text](url)`')

async def limits(client, message):
    await message.reply('No limits are currently enforced.')


def register(app):
    app.add_handler(MessageHandler(start, filters.command('start')))
    app.add_handler(MessageHandler(menu, filters.command('menu')))
    app.add_handler(MessageHandler(runs, filters.command('runs')))
    app.add_handler(MessageHandler(get_id, filters.command('id')))
    app.add_handler(MessageHandler(info, filters.command('info')))
    app.add_handler(MessageHandler(donate, filters.command('donate')))
    app.add_handler(MessageHandler(markdown_help, filters.command('markdownhelp')))
    app.add_handler(MessageHandler(limits, filters.command('limits')))
    app.add_handler(CallbackQueryHandler(panel_open, filters.regex('^[a-z]+:open$')))
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex('^main:menu$')))
