"""
Contextual system prompt node for the async flow pipeline.
"""

from datetime import UTC, datetime

from pocketflow import AsyncNode


class ContextualSystemPrompt(AsyncNode):
    def __init__(
        self, enable_contextual_system_prompt, genai_chat_system_prompt, history_limit
    ):
        super().__init__()
        self.enable_contextual_system_prompt = enable_contextual_system_prompt
        self.genai_chat_system_prompt = genai_chat_system_prompt
        self.history_limit = history_limit

    async def prep_async(self, shared):
        print("📝 [ContextualSystemPrompt] Preparing contextual system prompt")
        return {
            "participants": shared.get("unique_users", set()),
            "author_name": shared.get("author_name", "User"),
            "current_time": shared.get("created_at", datetime.now(UTC).isoformat()),
        }

    async def exec_async(self, prep_res):
        print(
            "🔧 [ContextualSystemPrompt] Processing system prompt with contextual information"
        )
        print(self.enable_contextual_system_prompt)
        # Check if contextual system prompt is enabled
        if not self.enable_contextual_system_prompt:
            print(
                "⏭️ [ContextualSystemPrompt] Contextual system prompt disabled, returning base prompt"
            )
            return self.genai_chat_system_prompt

        prep_res["participants"].add(prep_res["author_name"])

        # Build contextual information
        participants_str = (
            ", ".join(prep_res["participants"])
            if prep_res["participants"]
            else "Unknown"
        )

        contextual_system_prompt = f"""
Priority Contextual System Guidance:

You are an AI assistant with access to conversation context, including up to {self.history_limit} historical messages and relevant user information. You MUST use this information to personalize your responses naturally and accurately. Do NOT claim that you do not know personal details like the user's name, as you have been provided with this data—always incorporate it seamlessly without denying knowledge.

Your goal is to provide human-like responses tailored to the conversation's context. Remember and reference historical details from the provided records where relevant to make interactions feel continuous and personal.

Key information to use:
- You are talking to a human named {prep_res["author_name"]}. Always address or reference them by this name if appropriate, unless they specify otherwise.
- The conversation may involve one or more users. Current participants: {participants_str}.
- Current time: {prep_res["current_time"]}.
"""

        # Add contextual system prompt with clear labeling
        contextual_section = f"{contextual_system_prompt}"
        enhanced_prompt = f"{self.genai_chat_system_prompt}\n\n{contextual_section}"
        print(enhanced_prompt)
        print(
            "✅ [ContextualSystemPrompt] Enhanced system prompt with contextual information"
        )
        return enhanced_prompt

    async def post_async(self, shared, prep_res, exec_res):
        shared["enhanced_system_prompt"] = exec_res
        print(
            f"📝 [ContextualSystemPrompt] Enhanced system prompt stored, length: {len(exec_res)} characters"
        )
        return "success"
