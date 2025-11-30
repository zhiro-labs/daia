"""
LLM Router utility for supporting multiple AI providers.
"""

from google.genai import types


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


# Function mapping dictionary
PROVIDERS = {
    "gemini": _call_gemini,
}


async def call_llm(prompt: str, provider: str = "gemini", **kwargs) -> str:
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
