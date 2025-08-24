"""
LLM chat node for the async flow pipeline.
"""

from pocketflow import AsyncNode

from utils.llm_router import call_llm


class LLMChat(AsyncNode):
    def __init__(
        self, genai_client, chat_model, temperature, genai_tools, provider="gemini"
    ):
        super().__init__()
        self.genai_client = genai_client
        self.chat_model = chat_model
        self.temperature = temperature
        self.genai_tools = genai_tools
        self.provider = provider

    async def prep_async(self, shared):
        print(
            f"🤖 [LLMChat] Preparing chat with {len(shared.get('formatted_history', []))} history messages"
        )
        # Prepare the chat history and current message
        return {
            "formatted_history": shared.get("formatted_history", []),
            "current_message": shared.get("content", ""),
            "author_name": shared.get("author_name", "User"),  # unused?
            "enhanced_system_prompt": shared.get("enhanced_system_prompt"),
        }

    async def exec_async(self, prep_res):
        # Format current message with author context
        current_msg = f"{prep_res['author_name']}: {prep_res['current_message']}"
        print(f"💬 [LLMChat] Sending message: {current_msg[:100]}...")
        print(
            f"🔧 [LLMChat] Using provider: {self.provider}, model: {self.chat_model}, temperature: {self.temperature}"
        )

        # Use enhanced system prompt if available, otherwise fall back to base system prompt
        system_prompt = prep_res.get("enhanced_system_prompt")

        # Prepare kwargs for the LLM router
        llm_kwargs = {
            "client": self.genai_client,
            "model": self.chat_model,
            "temperature": self.temperature,
            "system_prompt": system_prompt,
            "history": prep_res["formatted_history"],
        }

        # Add provider-specific parameters
        if self.provider == "gemini":
            llm_kwargs["tools"] = [self.genai_tools] if self.genai_tools else []

        print(f"📤 [LLMChat] Sending message to {self.provider.upper()} LLM...")
        response = await call_llm(current_msg, provider=self.provider, **llm_kwargs)
        print(f"📥 [LLMChat] Received response: {response[:100]}...")
        return response

    async def post_async(self, shared, prep_res, exec_res):
        shared["llm_response"] = exec_res
        print(f"✅ [LLMChat] Response stored, length: {len(exec_res)} characters")
        return "success"
