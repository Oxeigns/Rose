from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

CAPTCHA_CHATS = set()

@Client.on_message(filters.command('captcha') & filters.group)
async def toggle_captcha(client, message):
    if message.chat.id in CAPTCHA_CHATS:
        CAPTCHA_CHATS.remove(message.chat.id)
        await message.reply('Captcha disabled.')
    else:
        CAPTCHA_CHATS.add(message.chat.id)
        await message.reply('Captcha enabled.')

@Client.on_message(filters.new_chat_members)
async def new_member(client, message):
    if message.chat.id not in CAPTCHA_CHATS:
        return
    for user in message.new_chat_members:
        btn = InlineKeyboardMarkup([[InlineKeyboardButton('Verify', callback_data=f'cverify:{user.id}')]])
        await message.reply(f'Welcome {user.mention}! Please verify.', reply_markup=btn)
        await client.restrict_chat_member(message.chat.id, user.id, can_send_messages=False)

@Client.on_callback_query(filters.regex(r'^cverify:(\d+)$'))
async def captcha_verify(client, query):
    user_id = int(query.data.split(':')[1])
    if query.from_user.id != user_id:
        await query.answer('Not for you.', show_alert=True)
        return
    await client.restrict_chat_member(query.message.chat.id, user_id, permissions=None)
    await query.message.delete()
    await query.answer('Verified!', show_alert=True)
