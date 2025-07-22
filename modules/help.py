from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

HELP_TEXT = "This is the help message from modules.help."

async def help_cmd(client: Client, message: Message):
    await message.reply_text(HELP_TEXT)

def register(app: Client) -> None:
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))
