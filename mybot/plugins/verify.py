from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import CHANNELS, LOG_GROUP
from database.mongo import settings_col


@Client.on_callback_query(filters.regex("^verify$"))
async def verify_join(client: Client, query: CallbackQuery):
    try:
        settings = await settings_col.find_one({"_id": "channels"}) or {}
        channels = settings.get("list", CHANNELS)
        missing = []
        for ch in channels:
            try:
                member = await client.get_chat_member(ch, query.from_user.id)
                if member.status in ("kicked", "left"):
                    missing.append(ch)
            except Exception:
                missing.append(ch)
        if missing:
            await query.answer("Please join all channels first!", show_alert=True)
        else:
            await query.answer("Verification successful!", show_alert=True)
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in verify_join: {e}")
        await query.answer("Error", show_alert=True)
