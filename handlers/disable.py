from pyrogram import Client, filters

@Client.on_message(filters.command('disable'))
async def placeholder(_, m):
    await m.reply('Disable module not implemented yet.')
