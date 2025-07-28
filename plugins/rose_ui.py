"""User interface module for basic bot panels."""

import logging
from typing import Dict, List

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from modules.constants import PREFIXES
from utils.errors import catch_errors

LOGGER = logging.getLogger(__name__)

# Help module data
HELP_ITEMS: Dict[str, Dict[str, List[str]]] = {
    "admin": {
        "desc": "Administrative tools for group moderators.",
        "cmds": ["/promote", "/demote"],
    },
    "bans": {
        "desc": "Ban and unban users quickly.",
        "cmds": ["/ban", "/unban"],
    },
    "filters": {
        "desc": "Create automated responses to keywords.",
        "cmds": ["/filter", "/stop"],
    },
    "notes": {
        "desc": "Save messages as notes for later.",
        "cmds": ["/save", "/note"],
    },
    "logging": {
        "desc": "Log important events to a channel.",
        "cmds": ["/logchannel"],
    },
}


# --- Panel builders ---

def start_panel(bot_name: str, is_group: bool = False) -> InlineKeyboardMarkup:
    """Generate the start/menu panel."""
    buttons: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton("Help", callback_data="ui_help")],
        [
            InlineKeyboardButton("Support", callback_data="ui_support"),
            InlineKeyboardButton("Developer", callback_data="ui_dev"),
        ],
    ]
    if is_group:
        buttons.append([InlineKeyboardButton("Settings", callback_data="ui_settings")])
    buttons.append([InlineKeyboardButton("Close", callback_data="ui_close")])
    return InlineKeyboardMarkup(buttons)


def help_menu() -> InlineKeyboardMarkup:
    """Build the help menu listing all modules."""
    keys: List[List[InlineKeyboardButton]] = []
    temp: List[InlineKeyboardButton] = []
    for mod in sorted(HELP_ITEMS.keys()):
        temp.append(InlineKeyboardButton(mod.title(), callback_data=f"help_module:{mod}"))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([
        InlineKeyboardButton("Back", callback_data="help_back"),
        InlineKeyboardButton("Close", callback_data="ui_close"),
    ])
    return InlineKeyboardMarkup(keys)


def module_buttons() -> InlineKeyboardMarkup:
    """Buttons for each module page."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Back", callback_data="help_back"),
                InlineKeyboardButton("Close", callback_data="ui_close"),
            ]
        ]
    )


def format_module_help(mod: str) -> str:
    """Format help text for a module."""
    data = HELP_ITEMS.get(mod)
    if not data:
        return "Module not found."
    cmds = "\n".join(data["cmds"])
    return f"**{mod.title()} Module**\n{data['desc']}\n\n{cmds}"


# --- Handlers ---

@catch_errors
async def start_cmd(client: Client, message: Message):
    bot = await client.get_me()
    is_group = message.chat.type in {"group", "supergroup"}
    text = f"**{bot.first_name}** at your service."
    await message.reply_text(
        text,
        reply_markup=start_panel(bot.first_name, is_group=is_group),
        parse_mode=ParseMode.MARKDOWN,
    )


menu_cmd = start_cmd


@catch_errors
async def help_cmd(client: Client, message: Message):
    await message.reply_text(
        "**Help Panel**",
        reply_markup=help_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )


# --- Callback query handlers ---

@catch_errors
async def help_open_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**Help Panel**",
        reply_markup=help_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


@catch_errors
async def support_cb(client: Client, query: CallbackQuery):
    await query.answer("Support: https://t.me/support_chat", show_alert=True)


@catch_errors
async def dev_cb(client: Client, query: CallbackQuery):
    await query.answer("Developer: https://t.me/oxeign", show_alert=True)


@catch_errors
async def settings_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**Group settings go here.**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="help_back"), InlineKeyboardButton("Close", callback_data="ui_close")]]
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


@catch_errors
async def module_cb(client: Client, query: CallbackQuery):
    mod = query.data.split(":")[1]
    await query.message.edit_text(
        format_module_help(mod),
        reply_markup=module_buttons(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


@catch_errors
async def back_cb(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "**Help Panel**",
        reply_markup=help_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await query.answer()


@catch_errors
async def close_cb(client: Client, query: CallbackQuery):
    await query.message.delete()
    await query.answer()


# --- Registration ---

def register(app: Client) -> None:
    LOGGER.info("Registering UI handlers")
    app.add_handler(MessageHandler(start_cmd, filters.command(["start", "menu"], prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(help_cmd, filters.command("help", prefixes=PREFIXES)), group=0)

    app.add_handler(CallbackQueryHandler(help_open_cb, filters.regex(r"^ui_help$")), group=0)
    app.add_handler(CallbackQueryHandler(support_cb, filters.regex(r"^ui_support$")), group=0)
    app.add_handler(CallbackQueryHandler(dev_cb, filters.regex(r"^ui_dev$")), group=0)
    app.add_handler(CallbackQueryHandler(settings_cb, filters.regex(r"^ui_settings$")), group=0)
    app.add_handler(CallbackQueryHandler(module_cb, filters.regex(r"^help_module:")), group=0)
    app.add_handler(CallbackQueryHandler(back_cb, filters.regex(r"^help_back$")), group=0)
    app.add_handler(CallbackQueryHandler(close_cb, filters.regex(r"^ui_close$")), group=0)

