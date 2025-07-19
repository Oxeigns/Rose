from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_panel():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("\u2795 Promote", callback_data="admin:promote"),
            InlineKeyboardButton("\u2796 Demote", callback_data="admin:demote"),
        ],
        [InlineKeyboardButton("\ud83d\udc65 Admins", callback_data="admin:list")],
        [InlineKeyboardButton("\u2b05\ufe0f Back", callback_data="main:menu")],
    ])
