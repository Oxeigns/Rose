import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

# Random run messages
RUN_STRINGS = [
    "Eeny meeny miny moe...",
    "Time to run away!",
    "Let's hide!",
    "Runs to the hills!",
    "🦶 Dashing off!"
]

async def runs(client: Client, message: Message):
    await message.reply_text(random.choice(RUN_STRINGS))

# /id command
async def get_id(client: Client, message: Message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    else:
        target = message.from_user

    await message.reply_text(f"🆔 ID: `{target.id}`", parse_mode="markdown")

# /info command
async def info(client: Client, message: Message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    text = f"**👤 User Info**\nName: {user.first_name}\nID: `{user.id}`"
    if user.username:
        text += f"\nUsername: @{user.username}"
    if user.bio:
        text += f"\nBio: {user.bio}"
    await message.reply_text(text, parse_mode="markdown")

# /donate command
async def donate(client: Client, message: Message):
    await message.reply_text(
        "[❤️ Donate here](https://example.com/donate) to support the bot's development!",
        disable_web_page_preview=True,
        parse_mode="markdown"
    )

# /markdownhelp command
async def markdown_help(client: Client, message: Message):
    if message.chat.type != "private":
        await message.reply("📬 I’ve sent you the Markdown guide in private.")
    await client.send_message(
        message.from_user.id,
        "**✏️ Markdown Guide**\nUse:\n- `*bold*`\n- `_italic_`\n- `[text](url)`",
        parse_mode="markdown"
    )

# /limits command
async def limits(client: Client, message: Message):
    await message.reply_text("🚫 No limits are currently enforced.")

# Register all handlers
def register(app: Client):
    app.add_handler(MessageHandler(runs, filters.command("runs")))
    app.add_handler(MessageHandler(get_id, filters.command("id")))
    app.add_handler(MessageHandler(info, filters.command("info")))
    app.add_handler(MessageHandler(donate, filters.command("donate")))
    app.add_handler(MessageHandler(markdown_help, filters.command("markdownhelp")))
    app.add_handler(MessageHandler(limits, filters.command("limits")))
