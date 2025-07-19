from pyrogram import Client, filters


@Client.on_message(filters.command('privacy'))
async def privacy_cmd(client, message):
    text = 'We only store data necessary for moderation. Use /delmydata to remove your info.'
    if message.chat.type != 'private':
        await message.reply('Check your PM for privacy info.')
        await client.send_message(message.from_user.id, text)
    else:
        await message.reply(text)


def register(app: Client):
    pass
