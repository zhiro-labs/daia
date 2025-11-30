"""
LLM chat node for the async flow pipeline.
"""

from pocketflow import AsyncNode

from utils import LLMConfig, call_llm


class LLMChat(AsyncNode):
    def __init__(self, config: LLMConfig):
        super().__init__()
        self.config = config

    async def prep_async(self, shared):
        print(
            f"🤖 [LLMChat] Preparing chat with {len(shared.get('formatted_history', []))} history messages"
        )
        return {
            "formatted_history": shared.get("formatted_history", []),
            "current_message": shared.get("content", ""),
            "author_name": shared.get("author_name", "User"),
            "enhanced_system_prompt": shared.get("enhanced_system_prompt"),
        }

    async def exec_async(self, prep_res):
        current_msg = f"{prep_res['author_name']}: {prep_res['current_message']}"
        print(f"💬 [LLMChat] Sending message: {current_msg[:100]}...")
        print(
            f"🔧 [LLMChat] Using provider: {self.config.provider}, model: {self.config.model}, temperature: {self.config.temperature}"
        )

        # Create a config copy with enhanced system prompt if available
        config = self.config
        if prep_res.get("enhanced_system_prompt"):
            config = LLMConfig(
                client=self.config.client,
                model=self.config.model,
                temperature=self.config.temperature,
                provider=self.config.provider,
                system_prompt=prep_res["enhanced_system_prompt"],
                tools=self.config.tools,
            )

        print(f"📤 [LLMChat] Sending message to {config.provider.upper()} LLM...")
        response = await call_llm(
            current_msg, config=config, history=prep_res["formatted_history"]
        )
        print(f"📥 [LLMChat] Received response: {response[:100]}...")
        return response

    async def post_async(self, shared, prep_res, exec_res):
        shared["llm_response"] = exec_res
        print(f"✅ [LLMChat] Response stored, length: {len(exec_res)} characters")
        return "success"
