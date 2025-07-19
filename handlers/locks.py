from pyrogram import Client, filters

@Client.on_message(filters.command('locks'))
async def placeholder(_, m):
    await m.reply('Locks module not implemented yet.')
