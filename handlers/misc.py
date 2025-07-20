import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Control panel button layout
MODULE_BUTTONS = [
    ("⚙️ Admin", "admin:open"),
    ("💬 Filters", "filters:open"),
    ("📜 Rules", "rules:open"),
    ("⚠️ Warnings", "warnings:open"),
    ("✅ Approvals", "approvals:open"),
    ("🔒 Lock", "lock:open"),
    ("📝 Notes", "notes:open"),
]


def build_menu() -> InlineKeyboardMarkup:
    """Return the main control panel keyboard."""

    keys = []
    temp = []
    for text, cb in MODULE_BUTTONS:
        temp.append(InlineKeyboardButton(text, callback_data=cb))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([InlineKeyboardButton("❌ Close", callback_data="main:close")])
    return InlineKeyboardMarkup(keys)

from buttons import (
    admin_panel,
    filters_panel,
    rules_panel,
    warnings_panel,
    approvals_panel,
    lock_panel,
    notes_panel,
)

MODULE_PANELS = {
    "admin": admin_panel,
    "filters": filters_panel,
    "rules": rules_panel,
    "warnings": warnings_panel,
    "approvals": approvals_panel,
    "lock": lock_panel,
    "notes": notes_panel,
}

# Start command
async def start(client: Client, message: Message):
    await message.reply_text(
        "**🌹 Rose Bot**\nI help moderate and protect your group.",
        reply_markup=build_menu(),
        quote=True,
    )

# Menu control panel
async def menu(client: Client, message: Message):
    await message.reply_text("**📋 Control Panel**", reply_markup=build_menu(), quote=True)

# Panel open handler
async def panel_open(client: Client, query: CallbackQuery):
    module = query.data.split(":")[0]
    panel_func = MODULE_PANELS.get(module)
    markup = panel_func() if panel_func else InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back", callback_data="main:menu")]]
    )
    await query.message.edit_text(
        f"**🔧 {module.title()} Panel**",
        reply_markup=markup,
        parse_mode="markdown",
    )
    await query.answer()

# Back to main menu
async def menu_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**📋 Control Panel**", reply_markup=build_menu(), parse_mode="markdown"
    )
    await query.answer()


# Close the panel
async def close_cb(client: Client, query: CallbackQuery):
    await query.message.delete()
    await query.answer()

# Random run messages
RUN_STRINGS = [
    "Eeny meeny miny moe...",
    "Time to run away!",
    "Let's hide!",
    "Runs to the hills!",
    "🦶 Dashing off!"
]

async def runs(client: Client, message: Message):
    await message.reply_text(random.choice(RUN_STRINGS))

# /id command
async def get_id(client: Client, message: Message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    else:
        target = message.from_user

    await message.reply_text(f"🆔 ID: `{target.id}`", parse_mode="markdown")

# /info command
async def info(client: Client, message: Message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    text = f"**👤 User Info**\nName: {user.first_name}\nID: `{user.id}`"
    if user.username:
        text += f"\nUsername: @{user.username}"
    if user.bio:
        text += f"\nBio: {user.bio}"
    await message.reply_text(text, parse_mode="markdown")

# /donate command
async def donate(client: Client, message: Message):
    await message.reply_text(
        "[❤️ Donate here](https://example.com/donate) to support the bot's development!",
        disable_web_page_preview=True,
        parse_mode="markdown"
    )

# /markdownhelp command
async def markdown_help(client: Client, message: Message):
    if message.chat.type != "private":
        await message.reply("📬 I’ve sent you the Markdown guide in private.")
    await client.send_message(
        message.from_user.id,
        "**✏️ Markdown Guide**\nUse:\n- `*bold*`\n- `_italic_`\n- `[text](url)`",
        parse_mode="markdown"
    )

# /limits command
async def limits(client: Client, message: Message):
    await message.reply_text("🚫 No limits are currently enforced.")

# Register all handlers
def register(app: Client):
    app.add_handler(MessageHandler(start, filters.command("start")))
    app.add_handler(MessageHandler(menu, filters.command("menu")))
    app.add_handler(MessageHandler(runs, filters.command("runs")))
    app.add_handler(MessageHandler(get_id, filters.command("id")))
    app.add_handler(MessageHandler(info, filters.command("info")))
    app.add_handler(MessageHandler(donate, filters.command("donate")))
    app.add_handler(MessageHandler(markdown_help, filters.command("markdownhelp")))
    app.add_handler(MessageHandler(limits, filters.command("limits")))

    app.add_handler(CallbackQueryHandler(panel_open, filters.regex("^[a-z]+:open$")))
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex("^main:menu$")))
    app.add_handler(CallbackQueryHandler(close_cb, filters.regex("^main:close$")))
