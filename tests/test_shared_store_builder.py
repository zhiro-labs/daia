from unittest.mock import MagicMock

import pytest

from utils.shared_store_builder import create_message_data, validate_message_data_types


@pytest.fixture
def mock_message():
    """Pytest fixture for a mock discord.Message object."""
    message = MagicMock()
    message.author.id = 123
    message.author.display_name = "Test User"
    message.channel.id = 456
    message.channel.name = "test-channel"
    message.id = 789
    message.content = "Hello, world!"
    message.embeds = []
    message.guild.id = 987
    message.guild.name = "Test Server"
    message.created_at.isoformat.return_value = "2025-08-23T12:00:00"
    message.attachments = []
    message.type = "default"
    return message


def test_create_message_data(mock_message):
    """Test the create_message_data function."""
    bot_user_id = 42
    message_data = create_message_data(mock_message, bot_user_id)

    assert message_data["author_id"] == 123
    assert message_data["author_name"] == "Test User"
    assert message_data["channel_id"] == 456
    assert message_data["message_id"] == 789
    assert message_data["content"] == "Hello, world!"
    assert message_data["bot_user_id"] == 42


def test_validate_message_data_types_valid():
    """Test validate_message_data_types with valid data."""
    valid_data = {
        "author_id": 123,
        "channel_id": 456,
        "message_id": 789,
        "bot_user_id": 42,
        "content": "hello",
        "author_name": "user",
        "channel_name": "channel",
        "guild_name": "guild",
        "timestamp": "2025-08-23T12:00:00",
        "embeds": [],
        "attachments": [],
    }
    assert validate_message_data_types(valid_data) is True


def test_validate_message_data_types_invalid():
    """Test validate_message_data_types with invalid data."""
    invalid_data = {
        "author_id": "123",  # Should be int
        "channel_id": 456,
        "message_id": 789,
        "bot_user_id": 42,
        "content": "hello",
        "author_name": "user",
        "channel_name": "channel",
        "guild_name": "guild",
        "timestamp": "2025-08-23T12:00:00",
        "embeds": [],
        "attachments": [],
    }
    assert validate_message_data_types(invalid_data) is False
