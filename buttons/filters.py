from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def filters_panel() -> InlineKeyboardMarkup:
    """Markup for the Filters module."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add", callback_data="filters:add"),
            InlineKeyboardButton("➖ Remove", callback_data="filters:remove"),
        ],
        [InlineKeyboardButton("📃 List", callback_data="filters:list")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
    ])
