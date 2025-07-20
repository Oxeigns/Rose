from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

HELP_MODULES = {
    "notes": "📝 **Notes**\nSave notes with `/save`, retrieve with `/get` or `#tag`, list all using `/notes`. Use `/clear` or `/clearall` to delete.",
    "purge": "🧹 **Purge**\nUse `/purge` to delete replied messages, `/purgefrom`, `/purgeto`, `/spurge`, or `/del` to clean ranges.",
    "pin": "📌 **Pin**\nUse `/pin`, `/unpin`, `/unpinall`, view `/pinned`. Tools: `/permapin`, `/antichannelpin`, `/cleanlinked`.",
    "topics": "💬 **Topics**\nManage forums: `/newtopic`, `/renametopic`, `/closetopic`, `/reopentopic`, `/deletetopic`, `/actiontopic`, `/setactiontopic`.",
    "warnings": "⚠️ **Warnings**\nWarn with `/warn`, remove with `/rmwarn` or `/resetwarn`. Configure: `/warnlimit`, `/warnmode`, `/warntime`.",
    "rules": "📜 **Rules**\nSet with `/setrules`, send button via `/setrulesbutton`. Use `/privaterules` to toggle PM mode.",
    "misc": "✨ **Misc**\n`/id`, `/info`, `/limits`, `/runs`, `/donate`, `/markdownhelp`, `/privacy`.",
    "locks": "🔒 **Locks**\nRestrict features via `/lock` or `/unlock`. Prevent spam, unwanted content, and more.",
    # Future extensions:
    "linkfilter": "🔗 **Link Filter**\n(Coming Soon) Block harmful or unwanted links using `/linkfilter` settings.",
    "biolink": "🧬 **Bio Link Filter**\n(Coming Soon) Detect unwanted links in user bios and take action.",
    "autodelete": "⏱️ **Auto Delete**\n(Coming Soon) Automatically delete messages after configured delay using `/cleancommand`.",
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
