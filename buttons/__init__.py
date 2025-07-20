"""Common inline button helpers used across modules."""

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BACK_TEXT = "⬅️ Back"
CLOSE_TEXT = "❌ Close"


def back_button(callback: str) -> InlineKeyboardMarkup:
    """Return a one-button markup with a Back button."""

    return InlineKeyboardMarkup([[InlineKeyboardButton(BACK_TEXT, callback_data=callback)]])


def close_button(callback: str = "main:close") -> InlineKeyboardMarkup:
    """Return a one-button markup with a Close button."""

    return InlineKeyboardMarkup([[InlineKeyboardButton(CLOSE_TEXT, callback_data=callback)]])

from .admin import admin_panel
from .notes import notes_panel
from .filters import filters_panel
from .rules import rules_panel
from .warnings import warnings_panel
from .approvals import approvals_panel
from .lock import lock_panel
