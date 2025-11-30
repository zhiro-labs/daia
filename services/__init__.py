"""
Services package for LLM and other external service integrations.
"""

from .llm_service import (
    get_chat_config,
    get_router_config,
    get_thinker_config,
    init_llm_configs,
)

__all__ = [
    "init_llm_configs",
    "get_chat_config",
    "get_router_config",
    "get_thinker_config",
]
