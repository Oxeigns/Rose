from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.markdown import escape_markdown
from utils.decorators import admin_required
FEDERATIONS = {}
GROUP_TO_FED = {}
USER_TO_FEDS = {}

@admin_required
async def create_fed(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: /createfed <fedname>')
        return
    fed_name = message.command[1]
    if fed_name in FEDERATIONS:
        await message.reply_text('❌ A federation with this name already exists.')
        return
    user_id = message.from_user.id
    FEDERATIONS[fed_name] = {'owner': user_id, 'banned_users': set()}
    USER_TO_FEDS.setdefault(user_id, set()).add(fed_name)
    safe = escape_markdown(fed_name)
    await message.reply_text(f'✅ Federation `{safe}` has been created.', parse_mode=ParseMode.MARKDOWN)

@admin_required
async def join_fed(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: /joinfed <fedname>')
        return
    fed_name = message.command[1]
    if fed_name not in FEDERATIONS:
        await message.reply_text('❌ Federation does not exist.')
        return
    GROUP_TO_FED[message.chat.id] = fed_name
    safe = escape_markdown(fed_name)
    await message.reply_text(f'✅ This group has joined the `{safe}` federation.', parse_mode=ParseMode.MARKDOWN)

@admin_required
async def leave_fed(client: Client, message: Message):
    if message.chat.id not in GROUP_TO_FED:
        await message.reply_text('❌ This group is not part of any federation.')
        return
    fed_name = GROUP_TO_FED.pop(message.chat.id)
    safe = escape_markdown(fed_name)
    await message.reply_text(f'🚪 Group left the `{safe}` federation.', parse_mode=ParseMode.MARKDOWN)

async def list_feds(client: Client, message: Message):
    user_id = message.from_user.id
    user_feds = USER_TO_FEDS.get(user_id, set())
    if not user_feds:
        await message.reply_text("🔍 You don't own or belong to any federations.")
        return
    text = '**📡 Your Federations:**\n'
    for fed in user_feds:
        text += f'• `{fed}`\n'
    await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

@admin_required
async def fed_ban(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to the user to fedban them.')
        return
    chat_id = message.chat.id
    fed_name = GROUP_TO_FED.get(chat_id)
    if not fed_name:
        await message.reply_text('❌ This group is not part of any federation.')
        return
    user_id = message.reply_to_message.from_user.id
    FEDERATIONS[fed_name]['banned_users'].add(user_id)
    safe = escape_markdown(fed_name)
    await message.reply_text(f'🚫 User `{user_id}` has been FedBanned in `{safe}`.', parse_mode=ParseMode.MARKDOWN)

@admin_required
async def fed_unban(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply to the user to fedunban them.')
        return
    chat_id = message.chat.id
    fed_name = GROUP_TO_FED.get(chat_id)
    if not fed_name:
        await message.reply_text('❌ This group is not part of any federation.')
        return
    user_id = message.reply_to_message.from_user.id
    FEDERATIONS[fed_name]['banned_users'].discard(user_id)
    safe = escape_markdown(fed_name)
    await message.reply_text(f'✅ User `{user_id}` has been FedUnbanned in `{safe}`.', parse_mode=ParseMode.MARKDOWN)

async def enforce_fedban(client: Client, message: Message):
    chat_id = message.chat.id
    fed_name = GROUP_TO_FED.get(chat_id)
    if not fed_name:
        return
    banned_users = FEDERATIONS[fed_name]['banned_users']
    for user in message.new_chat_members:
        if user.id in banned_users:
            try:
                await client.kick_chat_member(chat_id, user.id)
                await message.reply_text(f'⚠️ {user.mention} was FedBanned and removed.')
            except Exception:
                pass


def register(app):
    app.add_handler(MessageHandler(create_fed, filters.command('createfed', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(join_fed, filters.command('joinfed', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(leave_fed, filters.command('leavefed', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(list_feds, filters.command('federations', prefixes=PREFIXES)), group=0)
    app.add_handler(MessageHandler(fed_ban, filters.command('fedban', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(fed_unban, filters.command('fedunban', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(enforce_fedban, filters.new_chat_members), group=0)
