from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def approvals_panel() -> InlineKeyboardMarkup:
    """Markup for the Approvals module."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data="approvals:approve"),
            InlineKeyboardButton("🚫 Unapprove", callback_data="approvals:unapprove"),
        ],
        [InlineKeyboardButton("📋 List", callback_data="approvals:list")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
    ])
