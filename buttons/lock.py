from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def lock_panel() -> InlineKeyboardMarkup:
    """Markup for the Lock module."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔒 Lock", callback_data="lock:lock"),
            InlineKeyboardButton("🔓 Unlock", callback_data="lock:unlock"),
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
        [InlineKeyboardButton("❌ Close", callback_data="main:close")],
    ])
