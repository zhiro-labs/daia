"""
Runtime configuration management with YAML persistence.
Provides thread-safe access to dynamically editable configuration values.
"""

from pathlib import Path
from threading import Lock
from typing import Set

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
                "timezone": "UTC",
                "discord_activity": "Surfing",
            }
            self._save()
        else:
            with open(self.config_path, encoding="utf-8") as f:
                self._cache = yaml.safe_load(f) or {}

    def _save(self):
        """Save config to YAML file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._cache, f, default_flow_style=False, allow_unicode=True)

    @property
    def allowed_channels(self) -> Set[int]:
        """Get allowed channels as a set of integers (cached, no I/O)."""
        return set(self._cache.get("allowed_channels", []))

    @property
    def allowed_users(self) -> Set[int]:
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

    def add_channel(self, channel_id: int) -> bool:
        """
        Add a channel to allowed list.

        Args:
            channel_id: Discord channel ID to add

        Returns:
            bool: True if channel was added, False if already existed
        """
        with self._lock:
            channels = self._cache.get("allowed_channels", [])
            if channel_id not in channels:
                channels.append(channel_id)
                self._cache["allowed_channels"] = channels
                self._save()
                return True
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

    def add_user(self, user_id: int) -> bool:
        """
        Add a user to allowed DM list.

        Args:
            user_id: Discord user ID to add

        Returns:
            bool: True if user was added, False if already existed
        """
        with self._lock:
            users = self._cache.get("allowed_users", [])
            if user_id not in users:
                users.append(user_id)
                self._cache["allowed_users"] = users
                self._save()
                return True
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

    def reload(self):
        """Reload config from file (useful if manually edited)."""
        with self._lock:
            self._load()


# Global singleton instance
runtime_config = RuntimeConfig()
