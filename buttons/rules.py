from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rules_panel() -> InlineKeyboardMarkup:
    """Markup for the Rules module."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📜 View", callback_data="rules:view"),
            InlineKeyboardButton("📝 Set", callback_data="rules:set"),
        ],
        [InlineKeyboardButton("🔘 Button", callback_data="rules:button")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
        [InlineKeyboardButton("❌ Close", callback_data="main:close")],
    ])
