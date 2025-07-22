from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

async def start_cmd(client: Client, message: Message):
    await message.reply_text("Hello from modules.start!")

def register(app: Client) -> None:
    app.add_handler(MessageHandler(start_cmd, filters.command("start")))
