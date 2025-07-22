from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from handlers.start import help_cmd

def register(app: Client) -> None:
    """Register the /help command using the default handler."""
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))
