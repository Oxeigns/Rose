from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import OWNER_ID, LOG_GROUP
from database.mongo import settings_col, users_col


def owner_only(func):
    async def wrapper(client, message):
        if message.from_user.id != OWNER_ID:
            return
        return await func(client, message)
    return wrapper


def owner_cb(func):
    async def wrapper(client, query):
        if query.from_user.id != OWNER_ID:
            await query.answer("Unauthorized", show_alert=True)
            return
        return await func(client, query)
    return wrapper


@Client.on_message(filters.command("setbutton"))
@owner_only
async def setbutton(client: Client, message: Message):
    try:
        _, btn, value = message.text.split(maxsplit=2)
        await settings_col.update_one({"_id": btn}, {"$set": {"url": value}}, upsert=True)
        await message.reply_text("Button updated")
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in setbutton: {e}")


@Client.on_message(filters.command("setchannels"))
@owner_only
async def setchannels(client: Client, message: Message):
    try:
        channels = [c.strip() for c in message.text.split(None,1)[1].split(',') if c.strip()]
        await settings_col.update_one({"_id": "channels"}, {"$set": {"list": channels}}, upsert=True)
        await message.reply_text("Channels updated")
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in setchannels: {e}")


@Client.on_message(filters.command("points"))
@owner_only
async def points(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        data = await users_col.find_one({"_id": user_id}) or {"points": 0}
        await message.reply_text(f"User {user_id} has {data.get('points',0)} points")
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in points: {e}")


@Client.on_callback_query(filters.regex("^admin$"))
@owner_cb
async def admin_panel(client: Client, query: CallbackQuery):
    await query.answer("Admin features are command based", show_alert=True)

@Client.on_message(filters.command("approve"))
@owner_only
async def approve(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        await client.send_message(user_id, "Your withdrawal request is approved.")
        await message.reply_text("Approved")
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in approve: {e}")


@Client.on_message(filters.command("reject"))
@owner_only
async def reject(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        await client.send_message(user_id, "Your withdrawal request is rejected.")
        await message.reply_text("Rejected")
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in reject: {e}")

