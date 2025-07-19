from pyrogram import Client, filters
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting


@Client.on_message(filters.command('actiontopic') & filters.group)
async def action_topic(client, message):
    topic = get_chat_setting(message.chat.id, 'action_topic')
    if topic:
        await message.reply(f'Current action topic: {topic}')
    else:
        await message.reply('No action topic set.')


@Client.on_message(filters.command('setactiontopic') & filters.group)
@admin_required
async def set_action_topic(client, message):
    if message.reply_to_message:
        topic_id = message.reply_to_message.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        topic_id = int(message.command[1])
    else:
        await message.reply('Reply to a topic message or give topic id.')
        return
    set_chat_setting(message.chat.id, 'action_topic', str(topic_id))
    await message.reply('Action topic updated.')


@Client.on_message(filters.command('newtopic') & filters.group)
@admin_required
async def new_topic(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /newtopic <name>')
        return
    topic = await client.create_forum_topic(message.chat.id, message.command[1])
    await message.reply(f'Topic created with id {topic.message_thread_id}.')


@Client.on_message(filters.command('renametopic') & filters.group)
@admin_required
async def rename_topic(client, message):
    if len(message.command) < 2:
        await message.reply('Usage: /renametopic <name>')
        return
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('Use this in a topic or reply to topic.')
        return
    await client.edit_forum_topic(message.chat.id, topic_id, name=' '.join(message.command[1:]))
    await message.reply('Topic renamed.')


@Client.on_message(filters.command('closetopic') & filters.group)
@admin_required
async def close_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('Use this in a topic or reply to topic.')
        return
    await client.close_forum_topic(message.chat.id, topic_id)
    await message.reply('Topic closed.')


@Client.on_message(filters.command('reopentopic') & filters.group)
@admin_required
async def reopen_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('Use this in a topic or reply to topic.')
        return
    await client.reopen_forum_topic(message.chat.id, topic_id)
    await message.reply('Topic reopened.')


@Client.on_message(filters.command('deletetopic') & filters.group)
@admin_required
async def delete_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('Use this in a topic or reply to topic.')
        return
    await client.delete_forum_topic(message.chat.id, topic_id)
    await message.reply('Topic deleted.')


def register(app: Client):
    pass
