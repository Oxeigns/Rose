from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def warnings_panel() -> InlineKeyboardMarkup:
    """Markup for the Warnings module."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚠️ Warn", callback_data="warnings:warn"),
            InlineKeyboardButton("🔢 Limit", callback_data="warnings:limit"),
        ],
        [InlineKeyboardButton("⚙️ Settings", callback_data="warnings:settings")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
        [InlineKeyboardButton("❌ Close", callback_data="main:close")],
    ])
