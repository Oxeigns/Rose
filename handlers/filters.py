from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from utils.markdown import escape_markdown
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from buttons.filters import filters_panel
from utils.decorators import is_admin
from utils.db import add_filter, remove_filter, list_filters, get_filter, clear_filters


@is_admin
async def add_filter_cmd(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/filter <word> <response>`", parse_mode="markdown")
        return

    keyword = message.command[1].lower()
    response = " ".join(message.command[2:])

    add_filter(message.chat.id, keyword, response)
    safe_key = escape_markdown(keyword)
    await message.reply_text(
        f"✅ Filter `\"{safe_key}\"` added.", parse_mode="markdown"
    )


@is_admin
async def stop_filter_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/stop <word>`", parse_mode="markdown")
        return

    keyword = message.command[1].lower()
    remove_filter(message.chat.id, keyword)
    safe_key = escape_markdown(keyword)
    await message.reply_text(
        f"🗑️ Removed filter `\"{safe_key}\"`.", parse_mode="markdown"
    )


async def list_filters_cmd(client: Client, message: Message):
    words = list_filters(message.chat.id)
    if not words:
        await message.reply_text("❌ No filters have been set in this chat.")
    else:
        text = "**📃 Active Filters:**\n" + "\n".join(f"• `{w}`" for w in sorted(words))
        await message.reply_text(text, parse_mode="markdown")


@is_admin
async def stopall_cmd(client: Client, message: Message):
    clear_filters(message.chat.id)
    await message.reply_text("🧹 All filters cleared for this chat.")


async def filter_worker(client: Client, message: Message):
    if not message.text:
        return

    text = message.text.lower()
    for word in list_filters(message.chat.id):
        if word in text:
            response = get_filter(message.chat.id, word)
            if response:
                await message.reply_text(response)
            break


# Inline button callbacks for the Filters panel
async def filters_cb(client: Client, query: CallbackQuery):
    data = query.data.split(":")[1]
    if data == "add":
        text = "Use /filter word response to add a filter."
    elif data == "remove":
        text = "Use /stop word to remove a filter."
    elif data == "list":
        text = "Use /filters to list all filters."
    else:
        text = "Unknown command."
    await query.message.edit_text(text, reply_markup=filters_panel(), parse_mode="markdown")
    await query.answer()

def register(app: Client):
    app.add_handler(MessageHandler(add_filter_cmd, filters.command("filter") & filters.group))
    app.add_handler(MessageHandler(stop_filter_cmd, filters.command("stop") & filters.group))
    app.add_handler(MessageHandler(list_filters_cmd, filters.command("filters") & filters.group))
    app.add_handler(MessageHandler(stopall_cmd, filters.command("stopall") & filters.group))
    app.add_handler(MessageHandler(filter_worker, filters.text & filters.group), group=1)
    app.add_handler(CallbackQueryHandler(filters_cb, filters.regex(r"^filters:(?!open$).+")))
