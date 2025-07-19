from pyrogram import Client, filters

@Client.on_message(filters.command('privacy'))
async def placeholder(_, m):
    await m.reply('Privacy module not implemented yet.')
