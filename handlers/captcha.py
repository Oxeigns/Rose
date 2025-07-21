from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions,
)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
import asyncio

# Tracks groups where captcha is enabled
CAPTCHA_CHATS = set()
# Tracks pending verifications: (chat_id, user_id): message_id
PENDING = {}

@admin_required
async def toggle_captcha(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in CAPTCHA_CHATS:
        CAPTCHA_CHATS.remove(chat_id)
        await message.reply_text("❌ CAPTCHA has been disabled.")
    else:
        CAPTCHA_CHATS.add(chat_id)
        await message.reply_text("✅ CAPTCHA has been enabled.")

async def handle_new_user(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in CAPTCHA_CHATS:
        return

    for user in message.new_chat_members:
        if user.is_bot:
            continue

        try:
            # Restrict user from sending messages
            await client.restrict_chat_member(
                chat_id,
                user.id,
                ChatPermissions(can_send_messages=False)
            )

            # Send verification button
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ Verify", callback_data=f"cverify:{user.id}")]]
            )
            sent = await message.reply_text(
                f"👋 Welcome {user.mention}!\nPlease verify yourself to chat.",
                reply_markup=keyboard
            )

            # Save message to track it later for deletion
            PENDING[(chat_id, user.id)] = sent.message_id

            # Optional timeout cleanup
            await asyncio.sleep(180)  # 3 minutes
            if (chat_id, user.id) in PENDING:
                await client.kick_chat_member(chat_id, user.id)
                await sent.edit_text(f"⏱ {user.mention} failed to verify in time. Kicked.")

        except Exception as e:
            print(f"Captcha error: {e}")

async def captcha_verify(client: Client, query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    chat_id = query.message.chat.id

    if query.from_user.id != user_id:
        await query.answer("🚫 This verification isn’t for you.", show_alert=True)
        return

    try:
        # Unrestrict the verified user
        await client.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )
        )

        # Remove the verification message
        if (chat_id, user_id) in PENDING:
            del PENDING[(chat_id, user_id)]
        await query.message.delete()
        await query.answer("✅ You’ve been verified!", show_alert=True)

    except Exception as e:
        await query.answer("❌ Could not verify. Try again or contact admin.", show_alert=True)


def register(app: Client) -> None:
    app.add_handler(MessageHandler(toggle_captcha, filters.command("captcha") & filters.group))
    app.add_handler(MessageHandler(handle_new_user, filters.new_chat_members))
    app.add_handler(CallbackQueryHandler(captcha_verify, filters.regex(r"^cverify:(\d+)$")))
