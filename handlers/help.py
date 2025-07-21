"""Help module descriptions used by the start module."""

# Individual command descriptions for the help panel
HELP_MODULES = {
    "help": "Display this help message with inline buttons.",
    "id": "Get the ID of yourself or the replied user.",
    "info": "Show detailed information about a user.",
    "donate": "Display the donation link.",
    "markdownhelp": "Send a short guide about Markdown formatting.",
    "limits": "Show current bot limitations.",
    "runs": "Send a random running away message.",
    "ping": "Check bot responsiveness.",
    "echo": "Echo back your text.",
    "privacy": "Show the bot privacy policy.",

    "save": "Save a note. Reply or use `/save name text`.",
    "get": "Retrieve a note by name with `/get name` or `#name`.",
    "clear": "Delete a note by name.",
    "clearall": "Delete all notes in the chat.",
    "notes": "List all saved notes.",
    "privatenotes": "Toggle sending notes in PM instead of chat.",

    "purge": "Delete a range of messages starting from the reply.",
    "spurge": "Silently purge without a confirmation message.",
    "purgefrom": "Mark the beginning of a purge range.",
    "purgeto": "Purge messages from the marked point up to here.",
    "del": "Delete the replied message along with the command message.",

    "pin": "Pin a replied message (add 'loud' to notify).",
    "unpin": "Unpin the replied message or last pinned message.",
    "unpinall": "Unpin all pinned messages in the chat.",
    "permapin": "Send a message and pin it permanently.",
    "pinned": "Show the currently pinned message.",
    "antichannelpin": "Enable or disable auto-deleting channel pins.",
    "cleanlinked": "Enable or disable deleting 'linked to this message' notes.",

    "newtopic": "Create a new forum topic in groups with topics enabled.",
    "renametopic": "Rename the current forum topic.",
    "closetopic": "Close the current topic so users can't reply.",
    "reopentopic": "Reopen a closed topic.",
    "deletetopic": "Delete the current topic completely.",
    "actiontopic": "Show the current action logging topic ID.",
    "setactiontopic": "Set the action logging topic by reply or ID.",

    "warn": "Warn a user. After the limit a punishment is applied.",
    "dwarn": "Delete the replied message and warn the user.",
    "swarn": "Silently warn and delete the user's message.",
    "resetwarn": "Reset warnings for the replied user.",
    "rmwarn": "Remove one warning from the replied user.",
    "warns": "Show the number of warnings for a user.",
    "resetallwarns": "Reset all warnings in this chat.",
    "warnlimit": "Set how many warnings are allowed before action.",
    "warnmode": "Set punishment type when warn limit is reached.",
    "warntime": "Set how long the punishment lasts in seconds.",
    "warnings": "Display the current warning configuration.",

    "rules": "Show the group rules.",
    "setrules": "Set the group rules via text or reply.",
    "resetrules": "Remove the stored rules.",
    "setrulesbutton": "Set the label for the rules button under /rules.",
    "resetrulesbutton": "Remove the rules button label.",
    "privaterules": "Toggle sending rules in PM instead of chat.",

    "lock": "Lock a certain type of messages or actions in the chat.",

    "approve": "Approve a user to bypass restrictions.",
    "unapprove": "Revoke a previously approved user.",
    "approved": "List approved users in the chat.",
    "clearapproved": "Clear all approved users.",
    "approvalmode": "Toggle approval-only mode for regular users.",
}

# The actual /help command logic is now implemented in ``handlers.start``.
