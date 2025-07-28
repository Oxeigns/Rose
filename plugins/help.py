"""
Help Module
-----------
Provides:
- HELP_MODULES dictionary (for inline help panel in ui.py)
- Standalone /help handler (fallback if ui.py fails)
"""

import logging
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from utils.errors import catch_errors
from modules.constants import PREFIXES

# =====================================================
# HELP MODULES
# =====================================================

HELP_MODULES = {
    "help": "Display the help panel with inline buttons.",
    "id": "Get your user ID or the replied user's ID.",
    "info": "Show detailed profile information about a user.",
    "donate": "Show the donation link to support the bot.",
    "markdownhelp": "Guide on formatting text with Markdown.",
    "runs": "Fun command to make the bot 'run away'.",
    "limits": "Display bot usage limits.",
    "ping": "Check if the bot is online and responsive.",
    # Core features
    "admin": "Administrative tools for group moderators.",
    "filters": "Create and manage automated filters.",
    "rules": "Set or display the group rules.",
    "warnings": "Warn users and manage warning limits.",
    "approvals": "Allow trusted users to bypass restrictions.",
    "lock": "Restrict messages, media, or actions.",
    "notes": "Save and retrieve custom notes.",
    "greetings": "Send greetings to new members.",
    "connections": "Link groups/chats for shared actions.",
    "pinline": "Pin messages with an inline button.",
    "reports": "Enable members to report messages.",
}

LOGGER = logging.getLogger(__name__)

# =====================================================
# FALLBACK /HELP HANDLER
# =====================================================

@catch_errors
async def help_cmd(client, message):
    """
    Fallback /help handler:
    Used if ui.py is not loaded for some reason.
    Provides a simple static list of commands.
    """
    LOGGER.debug("Handling /help (standalone)")

    header = "**🛠 Available Modules**\n\n"
    body = "\n".join([f"- **{mod}** – {desc}" for mod, desc in HELP_MODULES.items()])
    footer = "\n\nFor an interactive menu, use `/help` in private."

    await message.reply_text(
        header + body + footer,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

# =====================================================
# REGISTRATION
# =====================================================

def register(app) -> None:
    """
    Registers the fallback /help command.
    This runs in a lower group priority so that
    ui.py's /help handler takes precedence.
    """
    LOGGER.info("Registering standalone /help from help.py")
    app.add_handler(
        MessageHandler(help_cmd, filters.command("help", prefixes=PREFIXES)),
        group=1  # runs only if group 0 (ui.py) doesn't handle it
    )
