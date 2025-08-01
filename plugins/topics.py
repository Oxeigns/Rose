from pyrogram import Client, filters
from modules.constants import PREFIXES
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting

async def action_topic(client, message):
    topic = get_chat_setting(message.chat.id, 'action_topic')
    if topic:
        await message.reply(f'📌 Current action topic ID: `{topic}`', quote=True)
    else:
        await message.reply('ℹ️ No action topic has been set yet.')

@admin_required
async def set_action_topic(client, message):
    if message.reply_to_message:
        topic_id = message.reply_to_message.message_thread_id or message.reply_to_message.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        topic_id = int(message.command[1])
    else:
        await message.reply('⚠️ Usage: Reply to a topic message or provide topic ID.')
        return
    set_chat_setting(message.chat.id, 'action_topic', str(topic_id))
    await message.reply('✅ Action topic has been set.')

@admin_required
async def new_topic(client, message):
    if len(message.command) < 2:
        await message.reply('⚠️ Usage: /newtopic <name>')
        return
    name = ' '.join(message.command[1:])
    try:
        topic = await client.create_forum_topic(message.chat.id, name)
        await message.reply(f'🆕 Topic created.\n🆔 ID: `{topic.message_thread_id}`')
    except Exception as e:
        await message.reply(f'❌ Failed to create topic:\n{e}')

@admin_required
async def rename_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('⚠️ Use this inside or reply to a topic.')
        return
    if len(message.command) < 2:
        await message.reply('⚠️ Usage: /renametopic <new name>')
        return
    name = ' '.join(message.command[1:])
    await client.edit_forum_topic(message.chat.id, topic_id, name=name)
    await message.reply('✏️ Topic renamed.')

@admin_required
async def close_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('⚠️ Use this inside or reply to a topic.')
        return
    await client.close_forum_topic(message.chat.id, topic_id)
    await message.reply('🔒 Topic closed.')

@admin_required
async def reopen_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('⚠️ Use this inside or reply to a topic.')
        return
    await client.reopen_forum_topic(message.chat.id, topic_id)
    await message.reply('🔓 Topic reopened.')

@admin_required
async def delete_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply('⚠️ Use this inside or reply to a topic.')
        return
    await client.delete_forum_topic(message.chat.id, topic_id)
    await message.reply('🗑️ Topic deleted.')


def register(app):
    app.add_handler(MessageHandler(action_topic, filters.command('actiontopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(set_action_topic, filters.command('setactiontopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(new_topic, filters.command('newtopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(rename_topic, filters.command('renametopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(close_topic, filters.command('closetopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(reopen_topic, filters.command('reopentopic', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(delete_topic, filters.command('deletetopic', prefixes=PREFIXES) & filters.group), group=0)
