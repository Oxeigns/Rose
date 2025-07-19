from pyrogram import Client, filters

@Client.on_message(filters.command('logchannel'))
async def placeholder(_, m):
    await m.reply('LogChannel module not implemented yet.')
