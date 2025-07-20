from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def back_button(callback: str) -> InlineKeyboardMarkup:
    """
    Create a simple inline 'Back' button.

    Args:
        callback (str): The callback_data to send when the button is pressed.

    Returns:
        InlineKeyboardMarkup: A one-button inline keyboard with a Back button.
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Back ⬅️", callback_data=callback)]
    ])
