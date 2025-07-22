from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from .start import help_cmd


def register(app: Client) -> None:
    """Register the /help command."""
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))
