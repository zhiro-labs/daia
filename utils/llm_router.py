"""
LLM Router utility for supporting multiple AI providers and use cases.
Supports chat, router, and thinker models with unified interface.
"""

from dataclasses import dataclass, field
from typing import Any

from google.genai import types


ANY_LLM_PREFIX = "any-llm-"


def parse_provider(provider: str) -> tuple[str, str | None]:
    """Parse provider string to extract base provider and sub-provider.

    Args:
        provider: Provider string (e.g., "gemini", "any-llm-openai")

    Returns:
        Tuple of (base_provider, sub_provider)
        - "gemini" → ("gemini", None)
        - "any-llm-openai" → ("any-llm", "openai")
        - "any-llm-anthropic" → ("any-llm", "anthropic")
    """
    if provider.startswith(ANY_LLM_PREFIX):
        sub_provider = provider[len(ANY_LLM_PREFIX) :]
        return ("any-llm", sub_provider if sub_provider else None)
    return (provider, None)


@dataclass
class LLMConfig:
    """Configuration for an LLM instance"""

    client: Any
    model: str
    temperature: float = 1.0
    provider: str = "gemini"
    system_prompt: str = ""
    tools: list = field(default_factory=list)

    @property
    def base_provider(self) -> str:
        """Get base provider (e.g., 'gemini' or 'any-llm')"""
        base, _ = parse_provider(self.provider)
        return base

    @property
    def sub_provider(self) -> str | None:
        """Get sub-provider for any-llm (e.g., 'openai', 'anthropic')"""
        _, sub = parse_provider(self.provider)
        return sub

    @property
    def is_any_llm(self) -> bool:
        """Check if using any-llm provider"""
        return self.provider.startswith(ANY_LLM_PREFIX)


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
    config: LLMConfig,
    history: list = None,
) -> str:
    """Unified LLM call interface

    Args:
        prompt: Input prompt
        config: LLMConfig instance
        history: Chat history (optional)

    Returns:
        Response from the LLM
    """
    base_provider = config.base_provider

    if base_provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {config.provider}. "
            f"Supported providers: {list(PROVIDERS.keys())}"
        )

    return await PROVIDERS[base_provider](prompt, config, history)


def get_supported_providers() -> list[str]:
    """Get list of supported providers"""
    return list(PROVIDERS.keys())
