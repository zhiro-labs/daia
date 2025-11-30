"""Discord slash commands module"""

from .admin_commands import setup_admin_commands
from .chat_commands import setup_chat_commands

__all__ = ["setup_admin_commands", "setup_chat_commands"]
