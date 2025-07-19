from pyrogram import Client, filters

@Client.on_message(filters.command('greetings'))
async def placeholder(_, m):
    await m.reply('Greetings module not implemented yet.')
