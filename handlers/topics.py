from pyrogram import Client, filters

@Client.on_message(filters.command('topics'))
async def placeholder(_, m):
    await m.reply('Topics module not implemented yet.')
