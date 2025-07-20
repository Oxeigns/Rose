from pyrogram import Client, filters
from pyrogram.types import Message
from utils.db import get_chat_setting, set_chat_setting
from utils.decorators import admin_required

# In-memory store for disabled commands (replace with DB in production)
DISABLED_CMDS = {}  # chat_id: set(command_names)

@Client.on_message(filters.command("disable") & filters.group)
@admin_required
async def disable_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/disable <command>`", parse_mode="markdown")
        return

    cmd = message.command[1].lower().lstrip("/")
    chat_id = message.chat.id

    DISABLED_CMDS.setdefault(chat_id, set()).add(cmd)
    await message.reply_text(f"🚫 Command `/{cmd}` has been disabled.", parse_mode="markdown")

@Client.on_message(filters.command("enable") & filters.group)
@admin_required
async def enable_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/enable <command>`", parse_mode="markdown")
        return

    cmd = message.command[1].lower().lstrip("/")
    chat_id = message.chat.id

    DISABLED_CMDS.setdefault(chat_id, set()).discard(cmd)
    await message.reply_text(f"✅ Command `/{cmd}` has been enabled.", parse_mode="markdown")

@Client.on_message(filters.command("disabled") & filters.group)
@admin_required
async def list_disabled(client: Client, message: Message):
    chat_id = message.chat.id
    disabled = DISABLED_CMDS.get(chat_id, set())

    if not disabled:
        await message.reply_text("✅ No commands are currently disabled.")
        return

    text = "**🚫 Disabled Commands:**\n"
    text += "\n".join(f"• `/{cmd}`" for cmd in sorted(disabled))
    await message.reply_text(text, parse_mode="markdown")

# Global filter hook to block disabled commands (lowest priority group)
@Client.on_message(filters.command("") & filters.group, group=-99)
async def block_disabled(client: Client, message: Message):
    chat_id = message.chat.id
    cmd = message.command[0].lower().lstrip("/")

    if cmd in DISABLED_CMDS.get(chat_id, set()):
        try:
            await message.delete()
        except Exception:
            pass
