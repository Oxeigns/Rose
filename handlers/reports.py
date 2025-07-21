from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.db import get_admins

REPORT_TAGS = {"@admin", "/report"}

# Reply-only report handler
async def handle_report(client: Client, message: Message):
    reported_msg = message.reply_to_message
    reporter = message.from_user
    chat = message.chat

    # Avoid self-reporting
    if reporter.id == reported_msg.from_user.id:
        await message.reply("❌ You can't report yourself.")
        return

    # Notify all admins (from DB or get_chat_administrators)
    admin_ids = await get_admin_ids(client, chat.id)
    if not admin_ids:
        await message.reply("⚠️ No admins found to report to.")
        return

    mention = reporter.mention(style="markdown")
    report_text = f"🚨 {mention} reported a message:\n\n"
    report_text += f"[Click to view message]({reported_msg.link})" if reported_msg.link else "Message replied above."

    try:
        await message.reply(report_text, parse_mode="markdown", disable_web_page_preview=True)
    except Exception:
        await message.reply("✅ Report submitted.")

# Utility to get list of admin IDs
async def get_admin_ids(client, chat_id):
    try:
        admins = await client.get_chat_members(chat_id, filter="administrators")
        return [admin.user.id for admin in admins if not admin.user.is_bot]
    except:
        return []


def register(app: Client) -> None:
    report_filter = filters.group & filters.reply & filters.text & (
        filters.regex(r"(?i)^@admin$") | filters.command("report")
    )
    app.add_handler(MessageHandler(handle_report, report_filter))
