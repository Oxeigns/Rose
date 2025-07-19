from pyrogram import Client, filters

@Client.on_message(filters.command('federations'))
async def placeholder(_, m):
    await m.reply('Federations module not implemented yet.')
