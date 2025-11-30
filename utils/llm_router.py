"""
LLM Router utility for supporting multiple AI providers and use cases.
Supports chat, router, and thinker models with unified interface.
"""

from dataclasses import dataclass, field
from typing import Any

from google.genai import types


@dataclass
class LLMConfig:
    """Configuration for an LLM instance"""

    client: Any
    model: str
    temperature: float = 1.0
    provider: str = "gemini"
    system_prompt: str = ""
    tools: list = field(default_factory=list)


async def _call_gemini(prompt: str, config: LLMConfig, history: list = None) -> str:
    """Call Google Gemini API"""
    if not config.client:
        raise ValueError("Gemini client is required")

    chat = config.client.aio.chats.create(
        model=config.model,
        config=types.GenerateContentConfig(
            system_instruction=config.system_prompt,
            temperature=float(config.temperature),
            tools=config.tools if config.tools else None,
        ),
        history=history or [],
    )

    response = await chat.send_message(prompt)
    return response.text


# Provider function mapping
PROVIDERS = {
    "gemini": _call_gemini,
}


async def call_llm(
    prompt: str,
    config: LLMConfig = None,
    history: list = None,
    # Legacy kwargs support for backward compatibility
    provider: str = None,
    **kwargs,
) -> str:
    """Unified LLM call interface

    Args:
        prompt: Input prompt
        config: LLMConfig instance (preferred)
        history: Chat history (optional)
        provider: Legacy provider string (deprecated, use config instead)
        **kwargs: Legacy kwargs (deprecated, use config instead)

    Returns:
        Response from the LLM
    """
    # Support legacy call pattern for backward compatibility
    if config is None:
        if provider is None:
            provider = "gemini"
        config = LLMConfig(
            client=kwargs.get("client"),
            model=kwargs.get("model", "gemini-1.5-flash"),
            temperature=kwargs.get("temperature", 1.0),
            provider=provider,
            system_prompt=kwargs.get("system_prompt", ""),
            tools=kwargs.get("tools", []),
        )
        history = kwargs.get("history", history)

    if config.provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {config.provider}. "
            f"Supported providers: {list(PROVIDERS.keys())}"
        )

    return await PROVIDERS[config.provider](prompt, config, history)


def get_supported_providers() -> list[str]:
    """Get list of supported providers"""
    return list(PROVIDERS.keys())
