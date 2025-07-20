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

from .admin import admin_panel
from .notes import notes_panel
from .filters import filters_panel
from .rules import rules_panel
from .warnings import warnings_panel
from .approvals import approvals_panel
from .lock import lock_panel
