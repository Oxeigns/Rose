from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def notes_panel() -> InlineKeyboardMarkup:
    """
    Returns the inline keyboard for the Notes module panel.

    Includes:
    - Example usage
    - Formatting help
    - Back to main menu
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📌 Example usage", callback_data="notes:example"),
            InlineKeyboardButton("🖋 Formatting", callback_data="notes:format"),
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="main:menu")],
        [InlineKeyboardButton("❌ Close", callback_data="main:close")]
    ])
