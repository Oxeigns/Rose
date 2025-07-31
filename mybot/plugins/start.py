from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, LOG_GROUP
from database.mongo import users_col, referrals_col, settings_col

START_IMG = "https://via.placeholder.com/600x200.png?text=Refer+%26+Earn"
START_CAPT = (
    "\ud83c\udfaf <b>Welcome to the Refer & Earn Bot</b>\n\n"
    "Invite friends and earn rewards!\n\n"
    "<b>1 Referral = 3 Points</b>\n"
    "<b>Minimum Withdrawal: 15 Points</b>"
)


async def start_keyboard(is_owner: bool = False):
    support = await settings_col.find_one({"_id": "support"})
    support_url = (support or {}).get("url", "https://t.me")
    buttons = [
        [
            InlineKeyboardButton("\ud83d\udc8e Referral", callback_data="referral"),
            InlineKeyboardButton("\ud83d\udcb0 Withdraw", callback_data="withdraw"),
        ],
        [InlineKeyboardButton("\u2705 Verify Join", callback_data="verify")],
        [
            InlineKeyboardButton("\ud83d\udcca My Points", callback_data="mypoints"),
            InlineKeyboardButton("\ud83c\udfc6 Top Users", callback_data="topusers"),
        ],
        [
            InlineKeyboardButton("\ud83d\udcdc Help", callback_data="help"),
            InlineKeyboardButton("\ud83d\udcac Support", url=support_url),
        ],
    ]
    if is_owner:
        buttons.append([InlineKeyboardButton("\ud83d\udee0 Admin Panel", callback_data="admin")])
    return InlineKeyboardMarkup(buttons)


@Client.on_message(filters.command("start"))
async def start(client, message):
    try:
        user = await users_col.find_one({"_id": message.from_user.id})
        is_owner = message.from_user.id == OWNER_ID
        if not user:
            await users_col.insert_one({"_id": message.from_user.id, "points": 0})
            parts = message.text.split(maxsplit=1)
            if len(parts) > 1:
                ref_id = int(parts[1]) if parts[1].isdigit() else None
                if ref_id and ref_id != message.from_user.id:
                    await referrals_col.insert_one({"from": ref_id, "to": message.from_user.id})
                    await users_col.update_one({"_id": ref_id}, {"$inc": {"points": 3}})
            await client.send_message(LOG_GROUP, f"#NEW_USER {message.from_user.mention} ({message.from_user.id})")
        keyboard = await start_keyboard(is_owner)
        await message.reply_photo(START_IMG, caption=START_CAPT, reply_markup=keyboard)
    except Exception as e:
        await client.send_message(LOG_GROUP, f"Error in /start: {e}")
