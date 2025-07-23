"""Register the `/help` command handler."""

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from .start import help_cmd


def register(app: Client) -> None:
    """Attach the help command handler to the given app."""
    app.add_handler(MessageHandler(help_cmd, filters.command("help")), group=0)

