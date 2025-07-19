from pyrogram import Client, filters

@Client.on_message(filters.command('cleancommands'))
async def placeholder(_, m):
    await m.reply('CleanCommands module not implemented yet.')
