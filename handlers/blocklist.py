from pyrogram import Client, filters

@Client.on_message(filters.command('blocklist'))
async def placeholder(_, m):
    await m.reply('Blocklist module not implemented yet.')
