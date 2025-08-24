"""
LLM Router utility for supporting multiple AI providers.
"""

import openai
from google.genai import types


async def _call_openai(prompt: str, **kwargs) -> str:
    """Call OpenAI API"""
    client = kwargs.get("client")
    model = kwargs.get("model", "gpt-3.5-turbo")
    temperature = kwargs.get("temperature", 0.7)
    system_prompt = kwargs.get("system_prompt", "")
    history = kwargs.get("history", [])

    if not client:
        raise ValueError("OpenAI client is required")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Add history messages
    messages.extend(history)

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )

    return response.choices[0].message.content


async def _call_gemini(prompt: str, **kwargs) -> str:
    """Call Google Gemini API"""
    client = kwargs.get("client")
    model = kwargs.get("model", "gemini-1.5-flash")
    temperature = kwargs.get("temperature", 1)
    system_prompt = kwargs.get("system_prompt", "")
    history = kwargs.get("history", [])
    tools = kwargs.get("tools", [])

    if not client:
        raise ValueError("Gemini client is required")

    chat = client.aio.chats.create(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=float(temperature),
            tools=tools if tools else None,
        ),
        history=history,
    )

    response = await chat.send_message(prompt)
    return response.text


async def _call_openai_compatible(prompt: str, **kwargs) -> str:
    """Call OpenAI-compatible API"""
    # This can be used for providers like Anthropic, Cohere, etc.
    # that follow OpenAI's API format
    base_url = kwargs.get("base_url")
    api_key = kwargs.get("api_key")
    model = kwargs.get("model", "gpt-5")
    temperature = kwargs.get("temperature", 0.7)
    system_prompt = kwargs.get("system_prompt", "")
    history = kwargs.get("history", [])

    if not base_url or not api_key:
        raise ValueError("base_url and api_key are required for OpenAI-compatible API")

    client = openai.AsyncOpenAI(base_url=base_url, api_key=api_key)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Add history messages
    messages.extend(history)

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )

    return response.choices[0].message.content


# Function mapping dictionary
PROVIDERS = {
    "openai": _call_openai,
    "gemini": _call_gemini,
    "openai_compatible": _call_openai_compatible,
}


async def call_llm(prompt: str, provider: str = "openai", **kwargs) -> str:
    """Call LLM with specified provider

    Args:
        prompt (str): Input prompt
        provider (str): LLM provider name
        **kwargs: Additional arguments for the specific provider

    Returns:
        str: Response from the LLM

    Raises:
        ValueError: If provider is not supported
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Supported providers: {list(PROVIDERS.keys())}"
        )

    func = PROVIDERS[provider]
    return await func(prompt, **kwargs)


def get_supported_providers() -> list[str]:
    """Get list of supported providers"""
    return list(PROVIDERS.keys())
