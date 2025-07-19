from pyrogram import Client, filters

@Client.on_message(filters.command('purge'))
async def placeholder(_, m):
    await m.reply('Purge module not implemented yet.')
