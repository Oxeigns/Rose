from pyrogram import Client, filters

@Client.on_message(filters.command('reports'))
async def placeholder(_, m):
    await m.reply('Reports module not implemented yet.')
