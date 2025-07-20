from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.decorators import admin_required
from pyrogram.types import CallbackQuery
from buttons.lock import lock_panel

# Define supported lock types and their corresponding permission flags
LOCK_MAP = {
    'messages': None,  # completely restrict user
    'media': 'can_send_media_messages',
    'sticker': 'can_send_stickers',
    'photo': 'can_send_photos',
    'video': 'can_send_videos',
    'voice': 'can_send_voice_notes',
    'audio': 'can_send_audios',
    'documents': 'can_send_documents',
    'polls': 'can_send_polls',
    'links': 'can_add_web_page_previews',
    'inline': 'can_use_inline_bots',
    'games': 'can_add_web_page_previews',  # same flag often used
    'invite': 'can_invite_users',
    'pin': 'can_pin_messages',
    'info': 'can_change_info',
}


def build_permissions(**kwargs):
    """Build a full ChatPermissions object with default True and overridden False."""
    perms = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_pin_messages=True,
        can_change_info=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_use_inline_bots=True,
    )
    for k, v in kwargs.items():
        setattr(perms, k, v)
    return perms


@admin_required
async def lock_cmd(client: Client, message: types.Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/lock <type>`", parse_mode="markdown")
        return

    lock_type = message.command[1].lower()
    if lock_type == 'messages':
        perms = types.ChatPermissions()  # completely restricts all messages
        await client.set_chat_permissions(message.chat.id, perms)
        await message.reply_text("🔒 Locked all messages.")
        return

    perm = LOCK_MAP.get(lock_type)
    if not perm:
        await message.reply_text("❌ Unknown lock type. Try `/lock media`, `/lock sticker`, etc.")
        return

    perms = build_permissions(**{perm: False})
    await client.set_chat_permissions(message.chat.id, perms)
    await message.reply_text(f"🔒 Locked `{lock_type}`.", parse_mode="markdown")


@admin_required
async def unlock_cmd(client: Client, message: types.Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/unlock <type>`", parse_mode="markdown")
        return

    lock_type = message.command[1].lower()
    if lock_type == 'messages':
        perms = build_permissions(can_send_messages=True)
        await client.set_chat_permissions(message.chat.id, perms)
        await message.reply_text("🔓 Unlocked all messages.")
        return

    perm = LOCK_MAP.get(lock_type)
    if not perm:
        await message.reply_text("❌ Unknown lock type.")
        return

    perms = build_permissions(**{perm: True})
    await client.set_chat_permissions(message.chat.id, perms)
    await message.reply_text(f"🔓 Unlocked `{lock_type}`.", parse_mode="markdown")


# Callbacks from lock panel
async def lock_cb(client: Client, query: CallbackQuery):
    data = query.data.split(":")[1]
    if data == "lock":
        text = "Use /lock <type> to lock something."
    elif data == "unlock":
        text = "Use /unlock <type> to unlock."
    else:
        text = "Unknown command."
    await query.message.edit_text(text, reply_markup=lock_panel(), parse_mode="markdown")
    await query.answer()


def register(app: Client):
    app.add_handler(MessageHandler(lock_cmd, filters.command("lock") & filters.group))
    app.add_handler(MessageHandler(unlock_cmd, filters.command("unlock") & filters.group))
    app.add_handler(CallbackQueryHandler(lock_cb, filters.regex(r"^lock:(?!open$).+")))
