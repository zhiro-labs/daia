"""
LLM Service - Centralized LLM configuration management.
Manages chat, router, and thinker model configurations.
"""

import os

from google import genai

from utils import LLMConfig

# Global config instances
_chat_config: LLMConfig | None = None
_router_config: LLMConfig | None = None
_thinker_config: LLMConfig | None = None


def _create_client(api_key: str | None):
    """Create a Gemini client if API key is provided"""
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def init_llm_configs(
    chat_system_prompt: str = "",
    chat_tools: list = None,
) -> None:
    """Initialize all LLM configurations from environment variables.

    Args:
        chat_system_prompt: System prompt for chat model
        chat_tools: Tools for chat model (e.g., Google Search)
    """
    global _chat_config, _router_config, _thinker_config

    # Chat model config
    chat_api_key = os.getenv("CHAT_MODEL_API_KEY")
    if chat_api_key:
        _chat_config = LLMConfig(
            client=_create_client(chat_api_key),
            model=os.getenv("CHAT_MODEL", "gemini-2.5-flash"),
            temperature=float(os.getenv("CHAT_TEMPERATURE", 1.0)),
            provider=os.getenv("CHAT_MODEL_PROVIDER", "gemini"),
            system_prompt=chat_system_prompt,
            tools=chat_tools or [],
        )

    # Router model config (low temperature for deterministic routing)
    router_api_key = os.getenv("ROUTER_MODEL_API_KEY")
    if router_api_key:
        _router_config = LLMConfig(
            client=_create_client(router_api_key),
            model=os.getenv("ROUTER_MODEL", "gemini-2.0-flash"),
            temperature=0.0,
            provider=os.getenv("ROUTER_MODEL_PROVIDER", "gemini"),
        )

    # Thinker model config
    thinker_api_key = os.getenv("THINKER_MODEL_API_KEY")
    if thinker_api_key:
        _thinker_config = LLMConfig(
            client=_create_client(thinker_api_key),
            model=os.getenv("THINKER_MODEL", "gemini-2.5-pro"),
            temperature=float(os.getenv("THINKER_TEMPERATURE", 0.7)),
            provider=os.getenv("THINKER_MODEL_PROVIDER", "gemini"),
        )


def get_chat_config() -> LLMConfig | None:
    """Get chat model configuration"""
    return _chat_config


def get_router_config() -> LLMConfig | None:
    """Get router model configuration"""
    return _router_config


def get_thinker_config() -> LLMConfig | None:
    """Get thinker model configuration"""
    return _thinker_config
