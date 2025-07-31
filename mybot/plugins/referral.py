from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import LOG_GROUP
from database.mongo import users_col


@Client.on_callback_query(filters.regex("^referral$"))
async def referral_cb(client: Client, query: CallbackQuery):
    try:
        user = query.from_user
        link = f"https://t.me/{client.me.username}?start={user.id}"
        data = await users_col.find_one({"_id": user.id}) or {"points": 0}
        text = (
            f"Share your link:\n<code>{link}</code>\n\n"
            f"You have <b>{data.get('points',0)}</b> points."
        )
        await query.message.edit_text(
            text,
            reply_markup=query.message.reply_markup,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in referral_cb: {e}")
        await query.answer("Error", show_alert=True)
