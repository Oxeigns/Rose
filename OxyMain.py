import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID", "12345"))
API_HASH = os.environ.get("API_HASH", "" )
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client(
    "rose_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

MODULES = [
    "Admin", "Antiflood", "Antiraid", "Approval", "Blocklist",
    "Captcha", "Clean Commands", "Connections", "Disable", "Federations",
    "Filters", "Formatting", "Greetings", "Import/Export", "Languages",
    "Locks", "Log Channel", "Misc", "Notes", "Pin", "Privacy",
    "Purge", "Reports", "Rules", "Topics", "Warnings"
]

HELP_TEXT = "\n".join(f"- {m}" for m in MODULES)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(
        "**Rose Bot**\nUse /menu to view modules.",
        quote=True,
    )

@app.on_message(filters.command("menu"))
async def menu(_, message):
    buttons = [
        [InlineKeyboardButton(m, callback_data=f"help:{m}")]
        for m in MODULES
    ]
    await message.reply(
        "**📚 Available Modules**",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
    )

@app.on_callback_query(filters.regex(r"^help:"))
async def help_cb(_, query):
    module = query.data.split(":", 1)[1]
    text = f"**{module} Module**\nWork in progress."
    await query.message.edit(text)
    await query.answer()

# Minimal Admin promotion example
@app.on_message(filters.command("promote") & filters.group)
async def promote(_, message):
    if not message.reply_to_message:
        await message.reply("Reply to a user to promote.")
        return
    try:
        await app.promote_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False,
        )
        await message.reply("User promoted.")
    except Exception as e:
        await message.reply(f"Failed to promote: {e}")

if __name__ == "__main__":
    app.run()
