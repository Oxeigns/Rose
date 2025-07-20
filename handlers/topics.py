from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from utils.decorators import admin_required
from utils.db import set_chat_setting, get_chat_setting


# /actiontopic – Get current topic set for logging/etc.
async def action_topic(client, message):
    topic = get_chat_setting(message.chat.id, 'action_topic')
    if topic:
        await message.reply(f"📌 Current action topic ID: `{topic}`", quote=True)
    else:
        await message.reply("ℹ️ No action topic has been set yet.")


# /setactiontopic – Set topic manually or by replying
@admin_required
async def set_action_topic(client, message):
    if message.reply_to_message:
        topic_id = message.reply_to_message.message_thread_id or message.reply_to_message.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        topic_id = int(message.command[1])
    else:
        await message.reply("⚠️ Usage: Reply to a topic message or provide topic ID.")
        return
    set_chat_setting(message.chat.id, 'action_topic', str(topic_id))
    await message.reply("✅ Action topic has been set.")


# /newtopic <name> – Create a new forum topic
@admin_required
async def new_topic(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /newtopic <name>")
        return
    name = ' '.join(message.command[1:])
    try:
        topic = await client.create_forum_topic(message.chat.id, name)
        await message.reply(f"🆕 Topic created.\n🆔 ID: `{topic.message_thread_id}`")
    except Exception as e:
        await message.reply(f"❌ Failed to create topic:\n{e}")


# /renametopic <new name>
@admin_required
async def rename_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply("⚠️ Use this inside or reply to a topic.")
        return
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /renametopic <new name>")
        return
    name = ' '.join(message.command[1:])
    await client.edit_forum_topic(message.chat.id, topic_id, name=name)
    await message.reply("✏️ Topic renamed.")


# /closetopic – Close a topic
@admin_required
async def close_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply("⚠️ Use this inside or reply to a topic.")
        return
    await client.close_forum_topic(message.chat.id, topic_id)
    await message.reply("🔒 Topic closed.")


# /reopentopic – Reopen a closed topic
@admin_required
async def reopen_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply("⚠️ Use this inside or reply to a topic.")
        return
    await client.reopen_forum_topic(message.chat.id, topic_id)
    await message.reply("🔓 Topic reopened.")


# /deletetopic – Delete a topic completely
@admin_required
async def delete_topic(client, message):
    topic_id = message.reply_to_message.message_thread_id if message.reply_to_message else message.message_thread_id
    if not topic_id:
        await message.reply("⚠️ Use this inside or reply to a topic.")
        return
    await client.delete_forum_topic(message.chat.id, topic_id)
    await message.reply("🗑️ Topic deleted.")


# Register all handlers
def register(app: Client):
    app.add_handler(MessageHandler(action_topic, filters.command('actiontopic') & filters.group))
    app.add_handler(MessageHandler(set_action_topic, filters.command('setactiontopic') & filters.group))
    app.add_handler(MessageHandler(new_topic, filters.command('newtopic') & filters.group))
    app.add_handler(MessageHandler(rename_topic, filters.command('renametopic') & filters.group))
    app.add_handler(MessageHandler(close_topic, filters.command('closetopic') & filters.group))
    app.add_handler(MessageHandler(reopen_topic, filters.command('reopentopic') & filters.group))
    app.add_handler(MessageHandler(delete_topic, filters.command('deletetopic') & filters.group))
