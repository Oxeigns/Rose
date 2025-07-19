from pyrogram import Client, filters

@Client.on_message(filters.command('antiraid'))
async def placeholder(_, m):
    await m.reply('Antiraid module not implemented yet.')
