from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

@Client.on_message(filters.command('privacy'))
async def privacy_cmd(client: Client, message):
    text = '**🔒 Privacy Policy**\n\nWe only store data required for moderation and functionality, such as:\n- Admin settings\n- Notes or filters saved by admins\n- Warning data\n\nYou can remove your personal data anytime with /delmydata.\nWe value your privacy and do not sell or share your data.'
    if message.chat.type != 'private':
        await message.reply("📩 I've sent you my privacy policy in PM.")
        try:
            await client.send_message(message.from_user.id, text, parse_mode='markdown')
        except Exception:
            await message.reply("❌ I can't message you. Please start me in PM first.")
    else:
        await message.reply(text, parse_mode='markdown')

@Client.on_message(filters.command('delmydata'))
async def del_my_data(client: Client, message):
    await message.reply('🗑️ Your data has been deleted from our systems (mock response).')
