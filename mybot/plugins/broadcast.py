from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, LOG_GROUP
from database.mongo import users_col


@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client: Client, message: Message):
    if len(message.command) < 2:
        return
    text = message.text.split(None, 1)[1]
    count = 0
    async for user in users_col.find({}):
        try:
            await client.send_message(user['_id'], text)
            count += 1
        except Exception:
            pass
    await message.reply_text(f"Broadcast sent to {count} users")
