from pyrogram import Client, filters

@Client.on_message(filters.command('pin'))
async def placeholder(_, m):
    await m.reply('Pin module not implemented yet.')
