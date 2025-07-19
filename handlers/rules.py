from pyrogram import Client, filters

@Client.on_message(filters.command('rules'))
async def placeholder(_, m):
    await m.reply('Rules module not implemented yet.')
