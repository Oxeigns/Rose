"""Help module: provides HELP_MODULES and registers a standalone /help handler."""

import logging
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from utils.errors import catch_errors
from modules.constants import PREFIXES

HELP_MODULES = {
    'help': 'Display this help message with inline buttons.',
    'id': 'Get the ID of yourself or the replied user.',
    'info': 'Show detailed information about a user.',
    'donate': 'Display the donation link.',
    'markdownhelp': 'Show how to format text using Markdown.',
    'runs': 'Run away from someone or something.',
    'limits': 'View the bot limits.',
    'ping': 'Check the bot is alive.',
    'admin': 'Administrative commands for group admins.',
    'filters': 'Manage filters for automated responses.',
    'rules': 'Set group rules.',
    'warnings': 'Warn users and track warning counts.',
    'approvals': 'Allow certain users to bypass locks.',
    'lock': 'Restrict certain message types or actions.',
    'notes': 'Save and retrieve notes.',
    'greetings': 'Greet new users.',
    'connections': 'Link chats together.',
    'pinline': 'Pin messages with an inline button.',
    'reports': 'Report messages to admins.',
}

LOGGER = logging.getLogger(__name__)

@catch_errors
async def help_cmd(client, message):
    """Standalone handler for /help command."""
    LOGGER.debug("📩 /help command handled by help.py")
    text = "**Available Modules:**\n\n"
    text += "\n".join([f"- `{mod}`: {desc}" for mod, desc in HELP_MODULES.items()])
    await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def register(app) -> None:
    """Register a simple /help handler to ensure help works even if ui.py fails."""
    LOGGER.info("Registering standalone help command from help.py")
    app.add_handler(
        MessageHandler(help_cmd, filters.command("help", prefixes=PREFIXES)),
        group=1
    )
