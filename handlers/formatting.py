from pyrogram import Client, filters

@Client.on_message(filters.command('formatting'))
async def placeholder(_, m):
    await m.reply('Formatting module not implemented yet.')
