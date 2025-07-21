from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from .help import HELP_MODULES
from buttons import (
    admin_panel,
    filters_panel,
    rules_panel,
    warnings_panel,
    approvals_panel,
    lock_panel,
    notes_panel,
)

# --------------------------------------------------
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

MODULE_PANELS = {
    "admin": admin_panel,
    "filters": filters_panel,
    "rules": rules_panel,
    "warnings": warnings_panel,
    "approvals": approvals_panel,
    "lock": lock_panel,
    "notes": notes_panel,
}


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


# --------------------------------------------------
# Help menu

def help_menu() -> InlineKeyboardMarkup:
    keys = []
    temp = []
    for mod in sorted(HELP_MODULES.keys()):
        temp.append(InlineKeyboardButton(mod.title(), callback_data=f"help:{mod}"))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([InlineKeyboardButton("❌ Close", callback_data="help:close")])
    return InlineKeyboardMarkup(keys)


# --------------------------------------------------
# Commands

async def start_cmd(client: Client, message: Message):
    await message.reply_text(
        "**🌹 Rose Bot**\nI help moderate and protect your group.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📋 Menu", callback_data="menu:open")]]
        ),
        quote=True,
    )


async def menu_cmd(client: Client, message: Message):
    await message.reply_text("**📋 Control Panel**", reply_markup=build_menu(), quote=True)


async def help_cmd(client: Client, message: Message):
    if len(message.command) > 1:
        mod = message.command[1].lower()
        if mod in HELP_MODULES:
            await message.reply_text(
                HELP_MODULES[mod], reply_markup=help_menu(), parse_mode="markdown"
            )
        else:
            await message.reply_text("❌ Unknown module.")
        return

    await message.reply_text(
        "**🛠 Help Panel**\nClick a button below to view module commands:",
        reply_markup=help_menu(),
        parse_mode="markdown",
    )


# --------------------------------------------------
# Callbacks

async def menu_open_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**📋 Control Panel**",
        reply_markup=build_menu(),
        parse_mode="markdown",
    )
    await query.answer()


async def panel_open_cb(client: Client, query: CallbackQuery):
    module = query.data.split(":")[0]
    panel_func = MODULE_PANELS.get(module)
    markup = (
        panel_func()
        if panel_func
        else InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main:menu")]])
    )
    await query.message.edit_text(
        f"**🔧 {module.title()} Panel**",
        reply_markup=markup,
        parse_mode="markdown",
    )
    await query.answer()


async def menu_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**📋 Control Panel**", reply_markup=build_menu(), parse_mode="markdown"
    )
    await query.answer()


async def close_cb(client: Client, query: CallbackQuery):
    await query.message.delete()
    await query.answer()


async def help_cb(client: Client, query: CallbackQuery):
    mod = query.data.split(":")[1]
    if mod == "close":
        await query.message.delete()
        return

    text = HELP_MODULES.get(mod, "❌ Module not found.")
    await query.message.edit_text(text, reply_markup=help_menu(), parse_mode="markdown")
    await query.answer()


# --------------------------------------------------
# Registration helper

def register(app: Client) -> None:
    app.add_handler(MessageHandler(start_cmd, filters.command("start")))
    app.add_handler(MessageHandler(menu_cmd, filters.command("menu")))
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))

    app.add_handler(CallbackQueryHandler(panel_open_cb, filters.regex("^[a-z]+:open$")))
    app.add_handler(CallbackQueryHandler(menu_open_cb, filters.regex("^menu:open$")))
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex("^main:menu$")))
    app.add_handler(CallbackQueryHandler(close_cb, filters.regex("^main:close$")))
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex(r"^help:.+")))
