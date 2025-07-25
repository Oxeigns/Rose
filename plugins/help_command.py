"""Register the `/help` command handler."""

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from .start import help_cmd
from modules.constants import PREFIXES


def register(app: Client) -> None:
    """Attach the help command handler to the given app."""
    app.add_handler(
        MessageHandler(help_cmd, filters.command("help", prefixes=PREFIXES)),
        group=0,
    )

