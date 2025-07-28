import logging
from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.db import get_admins
from pyrogram.errors import RPCError

REPORT_TAGS = {"@admin", "/report"}
LOGGER = logging.getLogger(__name__)

# Filter to catch reports either via @admin mention or /report command
report_filter = (
    filters.group
    & filters.reply
    & filters.text
    & (filters.regex(r"(?i)^@admin$") | filters.command("report", prefixes=PREFIXES))
)

async def handle_report(client: Client, message: Message):
    reported_msg = message.reply_to_message
    reporter = message.from_user
    chat = message.chat

    # Prevent self-report
    if reporter.id == reported_msg.from_user.id:
        await message.reply("❌ You can't report yourself.")
        return

    admin_ids = await get_admin_ids(client, chat.id)
    if not admin_ids:
        await message.reply("⚠️ No admins found to report to.")
        return

    mention = reporter.mention(style="markdown")
    report_text = f'🚨 {mention} reported a message:\n\n'
    report_text += (
        f'[Click to view message]({reported_msg.link})'
        if getattr(reported_msg, "link", None)
        else "Message replied above."
    )

    try:
        await message.reply(
            report_text,
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
    except RPCError as e:
        LOGGER.warning("Failed to send report message: %s", e)
        await message.reply("✅ Report submitted.")

async def get_admin_ids(client, chat_id):
    try:
        admins = await client.get_chat_members(chat_id, filter="administrators")
        return [admin.user.id for admin in admins if not admin.user.is_bot]
    except RPCError as e:
        LOGGER.warning("Failed to fetch admin list: %s", e)
        return []


def register(app):
    app.add_handler(MessageHandler(handle_report, report_filter), group=0)
