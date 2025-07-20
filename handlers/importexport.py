import json
from pyrogram import Client, filters
from pyrogram.types import Message, Document
from utils.decorators import admin_required
from utils.db import (
    export_chat_data,
    import_chat_data,
)

# Export data to JSON and send it as file
@Client.on_message(filters.command("export") & filters.group)
@admin_required
async def export_data(client: Client, message: Message):
    data = export_chat_data(message.chat.id)

    json_data = json.dumps(data, indent=2)
    await message.reply_document(
        document=("export.json", json_data.encode()),
        caption="📦 Exported group data (notes, filters, warns, etc.)"
    )


# Import JSON data back into current group
@Client.on_message(filters.command("import") & filters.group)
@admin_required
async def import_data(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply("❌ Please reply to a valid `.json` export file.")
        return

    doc: Document = message.reply_to_message.document
    if not doc.file_name.endswith(".json"):
        await message.reply("❌ Only `.json` files are supported.")
        return

    file_path = await client.download_media(doc)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        await message.reply(f"❌ Failed to parse JSON file:\n`{e}`", parse_mode="markdown")
        return

    count = import_chat_data(message.chat.id, data)
    await message.reply(f"✅ Imported `{count}` items successfully.", parse_mode="markdown")


# Optional help shortcut
@Client.on_message(filters.command("importexport") & filters.group)
async def importexport_help(client: Client, message: Message):
    text = (
        "**📤 Import & Export Help**\n\n"
        "`/export` - Get current group settings as `.json`\n"
        "`/import` - Reply to a `.json` file to restore settings\n\n"
        "_Only group admins can use this. Useful for backups and moving data._"
    )
    await message.reply_text(text, parse_mode="markdown")
