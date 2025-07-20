"""Utilities for Telegram Markdown formatting."""

def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram Markdown V2."""
    if not isinstance(text, str):
        return text
    for ch in ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"):
        text = text.replace(ch, f"\\{ch}")
    return text
