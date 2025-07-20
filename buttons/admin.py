from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel() -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard markup for admin controls.

    Includes:
    - Promote
    - Demote
    - List Admins
    - Back to main menu
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Promote", callback_data="admin:promote"),
            InlineKeyboardButton("➖ Demote", callback_data="admin:demote"),
        ],
        [InlineKeyboardButton("👥 Admins", callback_data="admin:list")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
    ])
