"""Help module descriptions used by the start module."""

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


def register(app) -> None:
    """This module only provides HELP_MODULES and registers no handlers."""
    pass
