"""
Tests to verify all modules can be imported successfully.
"""


def test_import_nodes():
    """Test that all node modules can be imported."""
    from nodes import (
        ContextualSystemPrompt,
        FetchDiscordHistory,
        LLMChat,
        MarkdownTableExtractor,
        ProcessMessageHistory,
        SendDiscordResponse,
        TableImageRenderer,
    )

    assert ContextualSystemPrompt is not None
    assert FetchDiscordHistory is not None
    assert LLMChat is not None
    assert MarkdownTableExtractor is not None
    assert ProcessMessageHistory is not None
    assert SendDiscordResponse is not None
    assert TableImageRenderer is not None


def test_import_utils():
    """Test that all utility modules can be imported."""
    from utils import (
        check_font_exists,
        create_message_data,
        env_onoff_to_bool,
        validate_message_data_types,
    )

    assert check_font_exists is not None
    assert create_message_data is not None
    assert env_onoff_to_bool is not None
    assert validate_message_data_types is not None


def test_import_llm_router():
    """Test that LLM router can be imported."""
    from utils.llm_router import call_llm, get_supported_providers

    assert call_llm is not None
    assert get_supported_providers is not None
