from pyrogram import Client, filters

@Client.on_message(filters.command('languages'))
async def placeholder(_, m):
    await m.reply('Languages module not implemented yet.')
