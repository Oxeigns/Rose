from pyrogram import Client, filters

@Client.on_message(filters.command('misc2'))
async def placeholder(_, m):
    await m.reply('Misc2 module not implemented yet.')
