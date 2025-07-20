from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

# Individual command descriptions for the help panel
HELP_MODULES = {
    "help": "Display this help message with inline buttons.",
    "id": "Get the ID of yourself or the replied user.",
    "info": "Show detailed information about a user.",
    "donate": "Display the donation link.",
    "markdownhelp": "Send a short guide about Markdown formatting.",
    "limits": "Show current bot limitations.",
    "runs": "Send a random running away message.",
    "privacy": "Show the bot privacy policy.",

    "save": "Save a note. Reply or use `/save name text`.",
    "get": "Retrieve a note by name with `/get name` or `#name`.",
    "clear": "Delete a note by name.",
    "clearall": "Delete all notes in the chat.",
    "notes": "List all saved notes.",
    "privatenotes": "Toggle sending notes in PM instead of chat.",

    "purge": "Delete a range of messages starting from the reply.",
    "spurge": "Silently purge without a confirmation message.",
    "purgefrom": "Mark the beginning of a purge range.",
    "purgeto": "Purge messages from the marked point up to here.",
    "del": "Delete the replied message along with the command message.",

    "pin": "Pin a replied message (add 'loud' to notify).",
    "unpin": "Unpin the replied message or last pinned message.",
    "unpinall": "Unpin all pinned messages in the chat.",
    "permapin": "Send a message and pin it permanently.",
    "pinned": "Show the currently pinned message.",
    "antichannelpin": "Enable or disable auto-deleting channel pins.",
    "cleanlinked": "Enable or disable deleting 'linked to this message' notes.",

    "newtopic": "Create a new forum topic in groups with topics enabled.",
    "renametopic": "Rename the current forum topic.",
    "closetopic": "Close the current topic so users can't reply.",
    "reopentopic": "Reopen a closed topic.",
    "deletetopic": "Delete the current topic completely.",
    "actiontopic": "Show the current action logging topic ID.",
    "setactiontopic": "Set the action logging topic by reply or ID.",

    "warn": "Warn a user. After the limit a punishment is applied.",
    "dwarn": "Delete the replied message and warn the user.",
    "swarn": "Silently warn and delete the user's message.",
    "resetwarn": "Reset warnings for the replied user.",
    "rmwarn": "Remove one warning from the replied user.",
    "warns": "Show the number of warnings for a user.",
    "resetallwarns": "Reset all warnings in this chat.",
    "warnlimit": "Set how many warnings are allowed before action.",
    "warnmode": "Set punishment type when warn limit is reached.",
    "warntime": "Set how long the punishment lasts in seconds.",
    "warnings": "Display the current warning configuration.",

    "rules": "Show the group rules.",
    "setrules": "Set the group rules via text or reply.",
    "resetrules": "Remove the stored rules.",
    "setrulesbutton": "Set the label for the rules button under /rules.",
    "resetrulesbutton": "Remove the rules button label.",
    "privaterules": "Toggle sending rules in PM instead of chat.",

    "lock": "Lock a certain type of messages or actions in the chat.",
}

# Dynamic help menu builder
def help_menu() -> InlineKeyboardMarkup:
    keys = []
    temp = []
    for i, mod in enumerate(sorted(HELP_MODULES.keys())):
        temp.append(InlineKeyboardButton(mod.title(), callback_data=f"help:{mod}"))
        if len(temp) == 2:
            keys.append(temp)
            temp = []
    if temp:
        keys.append(temp)
    keys.append([InlineKeyboardButton("❌ Close", callback_data="help:close")])
    return InlineKeyboardMarkup(keys)

# /help command
async def help_cmd(client: Client, message: Message):
    if len(message.command) > 1:
        mod = message.command[1].lower()
        if mod in HELP_MODULES:
            await message.reply_text(f"{HELP_MODULES[mod]}", reply_markup=help_menu(), parse_mode="markdown")
        else:
            await message.reply_text("❌ Unknown module.")
        return

    await message.reply_text(
        "**🛠 Help Panel**\nClick a button below to view module commands:",
        reply_markup=help_menu(),
        parse_mode="markdown"
    )

# Inline button callback
async def help_cb(client: Client, query: CallbackQuery):
    mod = query.data.split(":")[1]
    if mod == "close":
        await query.message.delete()
        return

    text = HELP_MODULES.get(mod, "❌ Module not found.")
    await query.message.edit_text(text, reply_markup=help_menu(), parse_mode="markdown")
    await query.answer()

# Register handlers
def register(app: Client):
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex(r"^help:.+")))
