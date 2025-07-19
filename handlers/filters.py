from pyrogram import Client, filters

@Client.on_message(filters.command('filters'))
async def placeholder(_, m):
    await m.reply('Filters module not implemented yet.')
