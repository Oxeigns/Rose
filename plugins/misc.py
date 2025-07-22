import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
RUN_STRINGS = ['Eeny meeny miny moe...', 'Time to run away!', "Let's hide!", 'Runs to the hills!', '🦶 Dashing off!']

@Client.on_message(filters.command('runs'))
async def runs(client: Client, message: Message):
    await message.reply_text(random.choice(RUN_STRINGS))

@Client.on_message(filters.command('id'))
async def get_id(client: Client, message: Message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    else:
        target = message.from_user
    await message.reply_text(f'🆔 ID: `{target.id}`', parse_mode='markdown')

@Client.on_message(filters.command('info'))
async def info(client: Client, message: Message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    text = f'**👤 User Info**\nName: {user.first_name}\nID: `{user.id}`'
    if user.username:
        text += f'\nUsername: @{user.username}'
    if user.bio:
        text += f'\nBio: {user.bio}'
    await message.reply_text(text, parse_mode='markdown')

@Client.on_message(filters.command('donate'))
async def donate(client: Client, message: Message):
    await message.reply_text("[❤️ Donate here](https://example.com/donate) to support the bot's development!", disable_web_page_preview=True, parse_mode='markdown')

@Client.on_message(filters.command('markdownhelp'))
async def markdown_help(client: Client, message: Message):
    if message.chat.type != 'private':
        await message.reply('📬 I’ve sent you the Markdown guide in private.')
    await client.send_message(message.from_user.id, '**✏️ Markdown Guide**\nUse:\n- `*bold*`\n- `_italic_`\n- `[text](url)`', parse_mode='markdown')

@Client.on_message(filters.command('limits'))
async def limits(client: Client, message: Message):
    await message.reply_text('🚫 No limits are currently enforced.')
