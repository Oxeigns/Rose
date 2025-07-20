from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


HELP_MODULES = {
    "notes": "Save notes with /save, get them with /get or #tag, list with /notes. Use /clear to remove and /clearall to wipe all.",
    "purge": "Delete messages quickly. Reply and use /purge <count>, /purgefrom, /purgeto, /spurge or /del.",
    "pin": "Manage pins. /pin, /unpin, /unpinall, /pinned, /permapin, /antichannelpin, /cleanlinked.",
    "topics": "Forum topic tools. /newtopic, /renametopic, /closetopic, /reopentopic, /deletetopic, /actiontopic, /setactiontopic.",
    "warnings": "Warn users with /warn, remove with /resetwarn or /rmwarn. Configure with /warnlimit, /warnmode and /warntime.",
    "rules": "Set chat rules with /setrules and a button with /setrulesbutton. Toggle PM sending with /privaterules.",
    "misc": "Misc commands: /donate, /runs, /id, /info, /limits, /markdownhelp, /privacy.",
    "locks": "Lock or unlock message types with /lock and /unlock.",
}


def help_menu():
    buttons = []
    row = []
    for i, mod in enumerate(sorted(HELP_MODULES)):
        row.append(InlineKeyboardButton(mod.title(), callback_data=f"help:{mod}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


async def help_cmd(client, message):
    if len(message.command) > 1:
        mod = message.command[1].lower()
        text = HELP_MODULES.get(mod, "Module not found.")
        await message.reply(text)
        return
    await message.reply("**Help Menu**", reply_markup=help_menu())


async def help_cb(client, query):
    mod = query.matches[0].group(1)
    text = HELP_MODULES.get(mod, "Module not found.")
    await query.message.edit(f"**{mod.title()}**\n{text}", reply_markup=help_menu())
    await query.answer()


def register(app: Client):
    app.add_handler(MessageHandler(help_cmd, filters.command("help")))
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex(r"^help:(.+)")))
