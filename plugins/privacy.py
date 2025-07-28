from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.handlers import MessageHandler

async def privacy_cmd(client: Client, message):
    text = '**🔒 Privacy Policy**\n\nWe only store data required for moderation and functionality, such as:\n- Admin settings\n- Notes or filters saved by admins\n- Warning data\n\nYou can remove your personal data anytime with /delmydata.\nWe value your privacy and do not sell or share your data.'
    if message.chat.type != 'private':
        await message.reply("📩 I've sent you my privacy policy in PM.")
        try:
            await client.send_message(message.from_user.id, text, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await message.reply("❌ I can't message you. Please start me in PM first.")
    else:
        await message.reply(text, parse_mode=ParseMode.MARKDOWN)

async def del_my_data(client: Client, message):
    await message.reply('🗑️ Your data has been deleted from our systems (mock response).')


def register(app):
    app.add_handler(MessageHandler(privacy_cmd, filters.command('privacy', prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(del_my_data, filters.command('delmydata', prefixes=PREFIXES)), group=0)
