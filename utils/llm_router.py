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
    api_key: str | None = None  # Used by any-llm provider

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


async def _call_any_llm(prompt: str, config: LLMConfig, history: list = None) -> str:
    """Call LLM via any-llm library (OpenAI-compatible interface)"""
    import asyncio
    import os

    from any_llm import completion

    if not config.sub_provider:
        raise ValueError("any-llm requires a sub-provider (e.g., 'any-llm-openai')")

    # Dynamically set the provider's env var if api_key is provided
    # any-llm checks for env vars during provider initialization
    if config.api_key:
        env_var_name = f"{config.sub_provider.upper()}_API_KEY"
        os.environ[env_var_name] = config.api_key

    # Build messages list in OpenAI format
    messages = []

    # Add system prompt if present
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})

    # Convert history to OpenAI format
    # History format varies by source, handle common cases
    if history:
        for msg in history:
            if isinstance(msg, dict):
                # Already in OpenAI format
                messages.append(msg)
            elif hasattr(msg, "role") and hasattr(msg, "parts"):
                # Gemini format: Content(role='user', parts=[Part(text='...')])
                role = "assistant" if msg.role == "model" else msg.role
                content = "".join(
                    part.text for part in msg.parts if hasattr(part, "text")
                )
                messages.append({"role": role, "content": content})

    # Add current prompt as user message
    messages.append({"role": "user", "content": prompt})

    # Build completion kwargs
    completion_kwargs = {
        "model": config.model,
        "provider": config.sub_provider,
        "messages": messages,
        "temperature": config.temperature,
    }

    # Add api_key if provided
    if config.api_key:
        completion_kwargs["api_key"] = config.api_key

    # Call any-llm (sync function, run in executor)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: completion(**completion_kwargs),
    )

    return response.choices[0].message.content


# Provider function mapping
PROVIDERS = {
    "gemini": _call_gemini,
    "any-llm": _call_any_llm,
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
