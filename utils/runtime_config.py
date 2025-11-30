"""
Runtime configuration management with YAML persistence.
Provides thread-safe access to dynamically editable configuration values.
"""

from pathlib import Path
from threading import Lock

import yaml


class RuntimeConfig:
    """Thread-safe runtime configuration with caching and YAML persistence."""

    def __init__(self, config_path: str = "config/runtime.yml"):
        self.config_path = Path(config_path)
        self._lock = Lock()
        self._cache = {}
        self._load()

    def _load(self):
        """Load config from YAML file, creating defaults if missing."""
        if not self.config_path.exists():
            # Create default config if it doesn't exist
            self._cache = {
                "allowed_channels": [],
                "allowed_users": [],
                "channel_metadata": {},
                "user_metadata": {},
                "timezone": "UTC",
                "discord_activity": "Surfing",
                "history_limit": 12,
            }
            self._save()
        else:
            with open(self.config_path, encoding="utf-8") as f:
                self._cache = yaml.safe_load(f) or {}
                # Ensure metadata dicts exist
                if "channel_metadata" not in self._cache:
                    self._cache["channel_metadata"] = {}
                if "user_metadata" not in self._cache:
                    self._cache["user_metadata"] = {}

    def _save(self):
        """Save config to YAML file with inline comments."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Build YAML content with comments manually
        lines = []
        lines.append("# Runtime configuration - can be modified via Discord commands\n")
        lines.append("# This file is auto-generated and will be updated by the bot\n\n")

        # Allowed channels with comments
        lines.append("# List of channel IDs where the bot is allowed to respond\n")
        lines.append("allowed_channels:\n")
        channels = self._cache.get("allowed_channels", [])
        channel_metadata = self._cache.get("channel_metadata", {})
        if not channels:
            lines.append("  []\n")
        else:
            for channel_id in channels:
                metadata = channel_metadata.get(str(channel_id), {})
                server = metadata.get("server", "Unknown Server")
                channel = metadata.get("channel", "Unknown Channel")
                lines.append(f"  - {channel_id}  # {server} / #{channel}\n")

        lines.append("\n")

        # Allowed users with comments
        lines.append("# List of user IDs allowed to DM the bot\n")
        lines.append("allowed_users:\n")
        users = self._cache.get("allowed_users", [])
        user_metadata = self._cache.get("user_metadata", {})
        if not users:
            lines.append("  []\n")
        else:
            for user_id in users:
                metadata = user_metadata.get(str(user_id), {})
                username = metadata.get("username", "Unknown User")
                lines.append(f"  - {user_id}  # {username}\n")

        lines.append("\n")

        # Metadata storage (hidden from main view)
        lines.append("# Metadata for human-readable comments (auto-managed)\n")
        lines.append("channel_metadata:\n")
        if not channel_metadata:
            lines.append("  {}\n")
        else:
            for channel_id, meta in channel_metadata.items():
                lines.append(f"  '{channel_id}':\n")
                lines.append(f"    server: {meta.get('server', 'Unknown')}\n")
                lines.append(f"    channel: {meta.get('channel', 'Unknown')}\n")

        lines.append("\n")
        lines.append("user_metadata:\n")
        if not user_metadata:
            lines.append("  {}\n")
        else:
            for user_id, meta in user_metadata.items():
                lines.append(f"  '{user_id}':\n")
                lines.append(f"    username: {meta.get('username', 'Unknown')}\n")

        lines.append("\n")

        # Other settings
        lines.append("# Timezone for bot operations\n")
        lines.append(f"timezone: {self._cache.get('timezone', 'UTC')}\n\n")

        lines.append("# Discord bot activity status message\n")
        lines.append(
            f"discord_activity: {self._cache.get('discord_activity', 'Surfing')}\n\n"
        )

        lines.append("# Number of messages to include in conversation history\n")
        lines.append(f"history_limit: {self._cache.get('history_limit', 12)}\n")

        with open(self.config_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    @property
    def allowed_channels(self) -> set[int]:
        """Get allowed channels as a set of integers (cached, no I/O)."""
        return set(self._cache.get("allowed_channels", []))

    @property
    def allowed_users(self) -> set[int]:
        """Get allowed users for DMs as a set of integers (cached, no I/O)."""
        return set(self._cache.get("allowed_users", []))

    @property
    def timezone(self) -> str:
        """Get configured timezone."""
        return self._cache.get("timezone", "UTC")

    @property
    def discord_activity(self) -> str:
        """Get Discord bot activity status."""
        return self._cache.get("discord_activity", "Surfing")

    @property
    def history_limit(self) -> int:
        """Get history limit for message context."""
        return self._cache.get("history_limit", 12)

    def add_channel(
        self, channel_id: int, server_name: str = None, channel_name: str = None
    ) -> bool:
        """
        Add a channel to allowed list.

        Args:
            channel_id: Discord channel ID to add
            server_name: Name of the server (optional, for comments)
            channel_name: Name of the channel (optional, for comments)

        Returns:
            bool: True if channel was added, False if already existed
        """
        with self._lock:
            channels = self._cache.get("allowed_channels", [])
            metadata = self._cache.get("channel_metadata", {})

            # Update metadata if provided (refreshes comments even if channel exists)
            if server_name or channel_name:
                metadata[str(channel_id)] = {
                    "server": server_name or "Unknown Server",
                    "channel": channel_name or "Unknown Channel",
                }
                self._cache["channel_metadata"] = metadata

            if channel_id not in channels:
                channels.append(channel_id)
                self._cache["allowed_channels"] = channels
                self._save()
                return True
            else:
                # Channel already exists, but save if metadata was updated
                if server_name or channel_name:
                    self._save()
                return False

    def remove_channel(self, channel_id: int) -> bool:
        """
        Remove a channel from allowed list.

        Args:
            channel_id: Discord channel ID to remove

        Returns:
            bool: True if channel was removed, False if didn't exist
        """
        with self._lock:
            channels = self._cache.get("allowed_channels", [])
            if channel_id in channels:
                channels.remove(channel_id)
                self._cache["allowed_channels"] = channels
                self._save()
                return True
            return False

    def add_user(self, user_id: int, username: str = None) -> bool:
        """
        Add a user to allowed DM list.

        Args:
            user_id: Discord user ID to add
            username: Username (optional, for comments)

        Returns:
            bool: True if user was added, False if already existed
        """
        with self._lock:
            users = self._cache.get("allowed_users", [])
            metadata = self._cache.get("user_metadata", {})

            # Update metadata if provided (refreshes comments even if user exists)
            if username:
                metadata[str(user_id)] = {"username": username}
                self._cache["user_metadata"] = metadata

            if user_id not in users:
                users.append(user_id)
                self._cache["allowed_users"] = users
                self._save()
                return True
            else:
                # User already exists, but save if metadata was updated
                if username:
                    self._save()
                return False

    def remove_user(self, user_id: int) -> bool:
        """
        Remove a user from allowed DM list.

        Args:
            user_id: Discord user ID to remove

        Returns:
            bool: True if user was removed, False if didn't exist
        """
        with self._lock:
            users = self._cache.get("allowed_users", [])
            if user_id in users:
                users.remove(user_id)
                self._cache["allowed_users"] = users
                self._save()
                return True
            return False

    def set_timezone(self, timezone: str):
        """Update timezone setting."""
        with self._lock:
            self._cache["timezone"] = timezone
            self._save()

    def set_discord_activity(self, activity: str):
        """Update Discord bot activity status."""
        with self._lock:
            self._cache["discord_activity"] = activity
            self._save()

    def set_history_limit(self, limit: int):
        """Update history limit for message context."""
        with self._lock:
            self._cache["history_limit"] = limit
            self._save()

    def reload(self):
        """Reload config from file (useful if manually edited)."""
        with self._lock:
            self._load()

    def update_channel_metadata(
        self, channel_id: int, server_name: str, channel_name: str
    ):
        """Update metadata for a specific channel without modifying allowed list."""
        with self._lock:
            metadata = self._cache.get("channel_metadata", {})
            metadata[str(channel_id)] = {"server": server_name, "channel": channel_name}
            self._cache["channel_metadata"] = metadata
            self._save()

    def update_user_metadata(self, user_id: int, username: str):
        """Update metadata for a specific user without modifying allowed list."""
        with self._lock:
            metadata = self._cache.get("user_metadata", {})
            metadata[str(user_id)] = {"username": username}
            self._cache["user_metadata"] = metadata
            self._save()

    def batch_update_metadata(self, channels: dict = None, users: dict = None):
        """
        Efficiently update multiple channel and user metadata in one operation.

        Args:
            channels: Dict of {channel_id: {"server": name, "channel": name}}
            users: Dict of {user_id: {"username": name}}
        """
        with self._lock:
            if channels:
                channel_metadata = self._cache.get("channel_metadata", {})
                for channel_id, data in channels.items():
                    channel_metadata[str(channel_id)] = data
                self._cache["channel_metadata"] = channel_metadata

            if users:
                user_metadata = self._cache.get("user_metadata", {})
                for user_id, data in users.items():
                    user_metadata[str(user_id)] = data
                self._cache["user_metadata"] = user_metadata

            # Only save once after all updates
            self._save()


# Global singleton instance
runtime_config = RuntimeConfig()
