"""
Tests for node modules.
"""

from unittest.mock import MagicMock

from nodes import (
    ContextualSystemPrompt,
    FetchDiscordHistory,
    LLMChat,
    MarkdownTableExtractor,
    ProcessMessageHistory,
    SendDiscordResponse,
    TableImageRenderer,
)


class TestFetchDiscordHistory:
    """Tests for FetchDiscordHistory node."""

    def test_init(self, mock_discord_bot):
        """Test FetchDiscordHistory initialization."""
        node = FetchDiscordHistory(mock_discord_bot, history_limit=10)
        assert node.bot == mock_discord_bot
        assert node.history_limit == 10


class TestProcessMessageHistory:
    """Tests for ProcessMessageHistory node."""

    def test_init(self):
        """Test ProcessMessageHistory initialization."""
        node = ProcessMessageHistory()
        assert node is not None


class TestContextualSystemPrompt:
    """Tests for ContextualSystemPrompt node."""

    def test_init_enabled(self):
        """Test ContextualSystemPrompt initialization when enabled."""
        system_prompt = "You are a helpful assistant."
        node = ContextualSystemPrompt(True, system_prompt, history_limit=10)
        assert node.enable_contextual_system_prompt is True
        assert node.genai_chat_system_prompt == system_prompt
        assert node.history_limit == 10

    def test_init_disabled(self):
        """Test ContextualSystemPrompt initialization when disabled."""
        system_prompt = "You are a helpful assistant."
        node = ContextualSystemPrompt(False, system_prompt, history_limit=10)
        assert node.enable_contextual_system_prompt is False


class TestLLMChat:
    """Tests for LLMChat node."""

    def test_init_with_config(self):
        """Test LLMChat initialization with LLMConfig."""
        from utils import LLMConfig

        mock_client = MagicMock()
        config = LLMConfig(
            client=mock_client,
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            provider="gemini",
        )
        node = LLMChat(config=config)
        assert node.config.client == mock_client
        assert node.config.model == "gemini-2.0-flash-exp"
        assert node.config.temperature == 0.7
        assert node.config.provider == "gemini"


class TestMarkdownTableExtractor:
    """Tests for MarkdownTableExtractor node."""

    def test_init(self):
        """Test MarkdownTableExtractor initialization."""
        node = MarkdownTableExtractor()
        assert node is not None


class TestTableImageRenderer:
    """Tests for TableImageRenderer node."""

    def test_init(self):
        """Test TableImageRenderer initialization."""
        node = TableImageRenderer()
        assert node is not None


class TestSendDiscordResponse:
    """Tests for SendDiscordResponse node."""

    def test_init(self, mock_discord_bot):
        """Test SendDiscordResponse initialization."""
        node = SendDiscordResponse(mock_discord_bot)
        assert node.bot == mock_discord_bot
