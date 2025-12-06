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


from utils.llm_router import ANY_LLM_PREFIX


def _create_client(api_key: str | None, provider: str = "gemini"):
    """Create a client based on provider type.

    For Gemini: creates a genai.Client
    For any-llm: returns a placeholder (any-llm uses env vars for API keys)
    """
    if provider.startswith(ANY_LLM_PREFIX):
        # any-llm doesn't need a client object, uses env vars
        # Return a placeholder to indicate config is valid
        return "any-llm"

    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def init_llm_configs(
    chat_system_prompt: str = "",
    chat_tools: list = None,
) -> None:
    """Initialize all LLM configurations from environment variables.

    Fallback logic:
    - Chat: uses env vars or defaults
    - Router/Thinker: uses own env vars → falls back to chat config

    Args:
        chat_system_prompt: System prompt for chat model
        chat_tools: Tools for chat model (e.g., Google Search)
    """
    global _chat_config, _router_config, _thinker_config

    # Default values for chat model
    default_model = "gemini-2.5-flash"
    default_provider = "gemini"
    default_temperature = 1.0

    # Chat model config
    chat_api_key = os.getenv("CHAT_MODEL_API_KEY")
    chat_model = os.getenv("CHAT_MODEL", default_model)
    chat_provider = os.getenv("CHAT_MODEL_PROVIDER", default_provider)
    chat_temperature = float(os.getenv("CHAT_TEMPERATURE", default_temperature))
    chat_client = _create_client(chat_api_key, chat_provider)

    if chat_client:
        _chat_config = LLMConfig(
            client=chat_client,
            model=chat_model,
            temperature=chat_temperature,
            provider=chat_provider,
            system_prompt=chat_system_prompt,
            tools=chat_tools or [],
            api_key=chat_api_key if chat_provider.startswith(ANY_LLM_PREFIX) else None,
        )

    # Router model config - falls back to chat config
    router_api_key = os.getenv("ROUTER_MODEL_API_KEY") or chat_api_key
    router_provider = os.getenv("ROUTER_MODEL_PROVIDER") or chat_provider
    router_client = (
        _create_client(router_api_key, router_provider)
        if router_api_key or router_provider.startswith(ANY_LLM_PREFIX)
        else chat_client
    )
    _router_config = (
        LLMConfig(
            client=router_client,
            model=os.getenv("ROUTER_MODEL") or chat_model,
            temperature=0.0,  # Router always uses low temperature
            provider=router_provider,
            api_key=router_api_key if router_provider.startswith(ANY_LLM_PREFIX) else None,
        )
        if router_client
        else None
    )

    # Thinker model config - falls back to chat config
    thinker_api_key = os.getenv("THINKER_MODEL_API_KEY") or chat_api_key
    thinker_provider = os.getenv("THINKER_MODEL_PROVIDER") or chat_provider
    thinker_client = (
        _create_client(thinker_api_key, thinker_provider)
        if thinker_api_key or thinker_provider.startswith(ANY_LLM_PREFIX)
        else chat_client
    )
    _thinker_config = (
        LLMConfig(
            client=thinker_client,
            model=os.getenv("THINKER_MODEL") or chat_model,
            temperature=float(os.getenv("THINKER_TEMPERATURE", 0.7)),
            provider=thinker_provider,
            api_key=thinker_api_key if thinker_provider.startswith(ANY_LLM_PREFIX) else None,
        )
        if thinker_client
        else None
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
