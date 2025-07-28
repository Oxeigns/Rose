"""
Telegram Bot UI Handlers for:
- /start
- /menu
- /help
- /test

This module builds the main control panel and help interface
for a Rose-style moderation bot.
"""

import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

# Inline help descriptions for each supported module
HELP_MODULES = {
    "help": "Display the help panel with inline buttons.",
    "id": "Get your user ID or the replied user's ID.",
    "info": "Show detailed profile information about a user.",
    "donate": "Show the donation link to support the bot.",
    "markdownhelp": "Guide on formatting text with Markdown.",
    "runs": "Fun command to make the bot 'run away'.",
    "limits": "Display bot usage limits.",
    "ping": "Check if the bot is online and responsive.",
    # Core features
    "admin": "Administrative tools for group moderators.",
    "filters": "Create and manage automated filters.",
    "rules": "Set or display the group rules.",
    "warnings": "Warn users and manage warning limits.",
    "approvals": "Allow trusted users to bypass restrictions.",
    "lock": "Restrict messages, media, or actions.",
    "notes": "Save and retrieve custom notes.",
    "greetings": "Send greetings to new members.",
    "connections": "Link groups/chats for shared actions.",
    "pinline": "Pin messages with an inline button.",
    "reports": "Enable members to report messages.",
}
from utils.errors import catch_errors
from modules.buttons import (
    admin_panel,
    approvals_panel,
    filters_panel,
    lock_panel,
    notes_panel,
    rules_panel,
    warnings_panel,
)
from modules.constants import PREFIXES
from db.broadcast import add_user

LOGGER = logging.getLogger(__name__)

# =====================================================
# PANEL CONFIGURATION
# =====================================================

MODULE_BUTTONS = [
    ("⚙️ Admin", "admin:open"),
    ("💬 Filters", "filters:open"),
    ("📜 Rules", "rules:open"),
    ("⚠️ Warnings", "warnings:open"),
    ("✅ Approvals", "approvals:open"),
    ("🔒 Lock", "lock:open"),
    ("📝 Notes", "notes:open"),
    ("ℹ️ Help", "help:main"),
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


# =====================================================
# UTILITY FUNCTIONS
# =====================================================

def _chunk_buttons(buttons, row_size=2):
    """Split buttons into rows of given size."""
    rows, temp = [], []
    for btn in buttons:
        temp.append(InlineKeyboardButton(*btn))
        if len(temp) == row_size:
            rows.append(temp)
            temp = []
    if temp:
        rows.append(temp)
    return rows


def build_menu() -> InlineKeyboardMarkup:
    """Main control panel menu."""
    rows = _chunk_buttons(MODULE_BUTTONS)
    rows.append([InlineKeyboardButton("❌ Close", callback_data="menu:close")])
    return InlineKeyboardMarkup(rows)


def help_menu() -> InlineKeyboardMarkup:
    """Help panel menu based on available modules."""
    buttons = []
    if HELP_MODULES:
        for mod in sorted(HELP_MODULES.keys(), key=str.lower):
            buttons.append((mod.title(), f"help:{mod}"))
    rows = _chunk_buttons(buttons)
    rows.append([
        InlineKeyboardButton("⬅️ Back", callback_data="menu:open"),
        InlineKeyboardButton("❌ Close", callback_data="help:close"),
    ])
    return InlineKeyboardMarkup(rows)


def log_command(message: Message):
    """Log commands in debug mode for traceability."""
    raw = getattr(message, "text", "")
    cmd = message.command[0] if hasattr(message, "command") and message.command else raw
    LOGGER.debug("Command: %s | Raw input: %s", cmd, raw)


async def _pm_user(client: Client, user_id: int, text: str, reply_markup=None):
    """Safely attempt to PM a user, with fallback logging."""
    try:
        await client.send_message(
            user_id,
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        LOGGER.warning("Unable to PM user %s: %s", user_id, e)
        return False
    return True


# =====================================================
# COMMAND HANDLERS
# =====================================================

@catch_errors
async def start_cmd(client: Client, message: Message):
    """Handle the /start command."""
    log_command(message)

    chat_type = getattr(message.chat, "type", "")
    user_id = getattr(message.from_user, "id", None)

    private_text = (
        "**🌹 Rose Bot**\n"
        "I help you manage, moderate, and secure your group.\n\n"
        "Use the menu below to configure my features."
    )

    group_text = (
        "**Thanks for adding me!**\n\n"
        "Use `/menu` here or open the PM I just sent you."
    )

    if chat_type == "private":
        if user_id:
            await add_user(user_id)
        await message.reply_text(
            private_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📋 Open Menu", callback_data="menu:open")]]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await message.reply_text(
            group_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📋 Open Menu", callback_data="menu:open")]]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        if user_id:
            success = await _pm_user(
                client,
                user_id,
                private_text,
                InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📋 Open Menu", callback_data="menu:open")]]
                ),
            )
            if not success:
                await message.reply("❌ Please start me in private to access settings.")


@catch_errors
async def menu_cmd(client: Client, message: Message):
    """Handle the /menu command."""
    log_command(message)
    await message.reply_text(
        "**📋 Control Panel**",
        reply_markup=build_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )


@catch_errors
async def help_cmd(client: Client, message: Message):
    """Handle the /help command."""
    log_command(message)

    cmd_parts = getattr(message, "command", [])
    mod = cmd_parts[1].lower() if len(cmd_parts) > 1 else None

    if mod and HELP_MODULES and mod in HELP_MODULES:
        response = HELP_MODULES[mod]
    elif mod:
        response = "❌ Unknown module.\nUse `/help` to see available modules."
    else:
        response = "**🛠 Help Panel**\nSelect a module to see its commands:"

    chat_type = getattr(message.chat, "type", "")
    user_id = getattr(message.from_user, "id", None)

    if chat_type == "private":
        await message.reply_text(
            response,
            reply_markup=help_menu(),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await message.reply("📩 I've sent you a PM with help information.")
        if user_id:
            success = await _pm_user(client, user_id, response, help_menu())
            if not success:
                await message.reply("❌ Please start me in private to access help.")


@catch_errors
async def test_cmd(client: Client, message: Message):
    """Handle /test command for quick responsiveness check."""
    log_command(message)

    chat_type = getattr(message.chat, "type", "")
    user_id = getattr(message.from_user, "id", None)

    if chat_type == "private":
        await message.reply_text("✅ Test command received!")
    else:
        await message.reply("📩 I've sent you a PM with the test result.")
        if user_id:
            success = await _pm_user(client, user_id, "✅ Test command received!")
            if not success:
                await message.reply("❌ Please start me in private first.")


# =====================================================
# CALLBACK HANDLERS
# =====================================================

async def menu_open_cb(client: Client, query: CallbackQuery):
    """Open the main control panel from any supported callback."""
    await query.message.edit_text(
        "**📋 Control Panel**",
        reply_markup=build_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


async def panel_open_cb(client: Client, query: CallbackQuery):
    module = query.data.split(":")[0]
    LOGGER.debug("Opening panel: %s", module)

    panel_func = MODULE_PANELS.get(module)
    markup = panel_func() if panel_func else InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back", callback_data="menu:open")]]
    )

    await query.message.edit_text(
        f"**🔧 {module.title()} Panel**",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


async def close_cb(client: Client, query: CallbackQuery):
    """Delete the menu message when the user presses Close."""
    await query.message.delete()
    await query.answer()


async def help_cb(client: Client, query: CallbackQuery):
    mod = query.data.split(":")[1]
    if mod == "close":
        await query.message.delete()
        await query.answer()
        return
    if mod == "main":
        await query.message.edit_text(
            "**🛠 Help Panel**\nSelect a module to see its commands:",
            reply_markup=help_menu(),
            parse_mode=ParseMode.MARKDOWN,
        )
        await query.answer()
        return
    text = HELP_MODULES.get(mod, "❌ Module not found.")
    await query.message.edit_text(
        text,
        reply_markup=help_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


# =====================================================
# REGISTRATION
# =====================================================

def register(app: Client):
    LOGGER.info("Registering handlers for start, menu, help, test")

    # Commands
    app.add_handler(MessageHandler(start_cmd, filters.command("start", PREFIXES)), group=0)
    app.add_handler(MessageHandler(menu_cmd, filters.command("menu", PREFIXES)), group=0)
    app.add_handler(MessageHandler(help_cmd, filters.command("help", PREFIXES)), group=0)
    app.add_handler(MessageHandler(test_cmd, filters.command("test", PREFIXES)), group=0)

    # Callbacks
    app.add_handler(
        CallbackQueryHandler(
            menu_open_cb,
            filters.regex(r"^(menu:open|main:menu)$"),
        ),
        group=0,
    )
    app.add_handler(
        CallbackQueryHandler(
            panel_open_cb,
            filters.regex(r"^(?!menu)[A-Za-z0-9_]+:open$"),
        ),
        group=0,
    )
    app.add_handler(
        CallbackQueryHandler(
            close_cb,
            filters.regex(r"^(menu:close|main:close)$"),
        ),
        group=0,
    )
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex(r"^help:.+")), group=0)
