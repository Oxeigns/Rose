from pyrogram import Client, filters
from utils.decorators import admin_required

@Client.on_message(filters.command('promote') & filters.group)
@admin_required
async def promote(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to promote.')
        return
    try:
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        await message.reply('User promoted.')
    except Exception as e:
        await message.reply(f'Failed to promote: {e}')

@Client.on_message(filters.command('demote') & filters.group)
@admin_required
async def demote(client, message):
    if not message.reply_to_message:
        await message.reply('Reply to a user to demote.')
        return
    try:
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        await message.reply('User demoted.')
    except Exception as e:
        await message.reply(f'Failed to demote: {e}')

@Client.on_message(filters.command('adminlist') & filters.group)
@admin_required
async def adminlist(client, message):
    members = await client.get_chat_members(message.chat.id, filter='administrators')
    text = '**Admins:**\n'
    async for m in members:
        text += f'- {m.user.mention}\n'
    await message.reply(text)
