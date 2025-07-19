from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def back_button(callback: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton('Back \u2b05\ufe0f', callback_data=callback)]])
