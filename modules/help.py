"""Module wrapper for /help command registration."""

from pyrogram import Client

from handlers.help_command import register as handler_register


def register(app: Client) -> None:
    """Delegate registration to ``handlers.help_command``."""
    handler_register(app)
