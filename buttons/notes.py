from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def notes_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Example usage', callback_data='notes:example'), InlineKeyboardButton('Formatting', callback_data='notes:format')],
        [InlineKeyboardButton('Back', callback_data='main:menu')]
    ])
