"""
Tests for utility functions.
"""

from utils import (
    check_font_exists,
    create_message_data,
    env_onoff_to_bool,
    validate_message_data_types,
)


class TestConfigUtils:
    """Tests for config_utils module."""

    def test_env_onoff_to_bool_on(self):
        """Test env_onoff_to_bool with 'on' value."""
        assert env_onoff_to_bool("on") is True
        assert env_onoff_to_bool("ON") is True

    def test_env_onoff_to_bool_off(self):
        """Test env_onoff_to_bool with 'off' value."""
        assert env_onoff_to_bool("off") is False
        assert env_onoff_to_bool("OFF") is False

    def test_env_onoff_to_bool_invalid(self):
        """Test env_onoff_to_bool with invalid value."""
        assert env_onoff_to_bool("invalid") is False
        assert env_onoff_to_bool("") is False
        assert env_onoff_to_bool(None) is False


class TestSharedStoreBuilder:
    """Tests for shared_store_builder module."""

    def test_create_message_data(self, mock_discord_message):
        """Test create_message_data function."""
        bot_user_id = 999888777
        result = create_message_data(mock_discord_message, bot_user_id)

        assert result["author_id"] == mock_discord_message.author.id
        assert result["author_name"] == mock_discord_message.author.display_name
        assert result["channel_id"] == mock_discord_message.channel.id
        assert result["message_id"] == mock_discord_message.id
        assert result["bot_user_id"] == bot_user_id

    def test_validate_message_data_types_valid(self, sample_message_data):
        """Test validate_message_data_types with valid data."""
        assert validate_message_data_types(sample_message_data) is True

    def test_validate_message_data_types_invalid(self):
        """Test validate_message_data_types with invalid data."""
        invalid_data = {
            "author_id": "not_an_int",
            "author_name": "TestUser",
            "channel_id": 987654321,
            "message_id": 111222333,
            "bot_user_id": 999888777,
        }
        assert validate_message_data_types(invalid_data) is False


class TestDownloadFont:
    """Tests for download_font module."""

    def test_check_font_exists_returns_bool(self):
        """Test check_font_exists returns a boolean value."""
        result = check_font_exists()
        assert isinstance(result, bool)
