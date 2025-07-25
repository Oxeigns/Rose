from pyrogram import Client, filters, StopPropagation
from modules.constants import PREFIXES
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from utils.db import get_chat_setting, set_chat_setting
from utils.decorators import admin_required
DISABLED_CMDS = {}

@admin_required
async def disable_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/disable <command>`', parse_mode='markdown')
        return
    cmd = message.command[1].lower().lstrip('/')
    chat_id = message.chat.id
    DISABLED_CMDS.setdefault(chat_id, set()).add(cmd)
    await message.reply_text(f'🚫 Command `/{cmd}` has been disabled.', parse_mode='markdown')

@admin_required
async def enable_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Usage: `/enable <command>`', parse_mode='markdown')
        return
    cmd = message.command[1].lower().lstrip('/')
    chat_id = message.chat.id
    DISABLED_CMDS.setdefault(chat_id, set()).discard(cmd)
    await message.reply_text(f'✅ Command `/{cmd}` has been enabled.', parse_mode='markdown')

@admin_required
async def list_disabled(client: Client, message: Message):
    chat_id = message.chat.id
    disabled = DISABLED_CMDS.get(chat_id, set())
    if not disabled:
        await message.reply_text('✅ No commands are currently disabled.')
        return
    text = '**🚫 Disabled Commands:**\n'
    text += '\n'.join((f'• `/{cmd}`' for cmd in sorted(disabled)))
    await message.reply_text(text, parse_mode='markdown')

async def block_disabled(client: Client, message: Message):
    chat_id = message.chat.id
    cmd = message.command[0].lower().lstrip('/')
    if cmd in DISABLED_CMDS.get(chat_id, set()):
        try:
            await message.delete()
        except Exception:
            pass
        raise StopPropagation


def register(app):
    app.add_handler(MessageHandler(disable_command, filters.command('disable', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(enable_command, filters.command('enable', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(list_disabled, filters.command('disabled', prefixes=PREFIXES) & filters.group), group=0)
    app.add_handler(MessageHandler(block_disabled, filters.command('', prefixes=PREFIXES) & filters.group), group=-99)

