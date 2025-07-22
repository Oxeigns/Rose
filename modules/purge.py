from pyrogram import Client
from handlers.purge import register as handler_register

def register(app: Client) -> None:
    handler_register(app)
