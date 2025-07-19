from pyrogram import Client, filters

@Client.on_message(filters.command('approval'))
async def placeholder(_, m):
    await m.reply('Approval module not implemented yet.')
