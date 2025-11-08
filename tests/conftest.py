"""
Pytest configuration and shared fixtures.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        "DISCORD_BOT_TOKEN": "test_discord_token",
        "DISCORD_BOT_ACTIVITY": "Testing",
        "ALLOWED_CHANNELS": "123456789,987654321",
        "HISTORY_LIMIT": "10",
        "GEMINI_API_KEY": "test_gemini_key",
        "CHAT_MODEL": "gemini-2.0-flash-exp",
        "CHAT_TEMPERATURE": "0.7",
        "CHAT_SYS_PROMPT_PATH": "config/chat_sys_prompt.txt.example",
        "ENABLE_CONTEXTUAL_SYSTEM_PROMPT": "on",
        "CHAT_MODEL_PROVIDER": "gemini",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_discord_message():
    """Create a mock Discord message object."""
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 123456789
    message.author.display_name = "TestUser"
    message.author.name = "testuser"
    message.channel = MagicMock()
    message.channel.id = 987654321
    message.channel.name = "test-channel"
    message.id = 111222333
    message.content = "Hello bot!"
    message.created_at = MagicMock()
    return message


@pytest.fixture
def mock_discord_bot():
    """Create a mock Discord bot object."""
    bot = MagicMock()
    bot.user = MagicMock()
    bot.user.id = 999888777
    bot.user.name = "TestBot"
    bot.get_channel = AsyncMock()
    return bot


@pytest.fixture
def sample_message_data():
    """Create sample message data for testing."""
    return {
        "author_id": 123456789,
        "author_name": "TestUser",
        "channel_id": 987654321,
        "message_id": 111222333,
        "bot_user_id": 999888777,
    }
