"""
Discord history fetching node for the async flow pipeline.
"""

import aiohttp
import discord
from pocketflow import AsyncNode


class FetchDiscordHistory(AsyncNode):
    def __init__(self, bot=None, history_limit=12):
        super().__init__()
        self.bot = bot
        self.history_limit = history_limit

    async def prep_async(self, shared):
        print("🔍 [FetchDiscordHistory] Starting prep_async")
        print(f"🔍 [FetchDiscordHistory] Input shared data: {shared}")
        print(
            f"🔍 [FetchDiscordHistory] Preparing to fetch history for channel {shared['channel_id']}, message {shared['message_id']}"
        )

        prep_result = {
            "channel_id": shared["channel_id"],
            "message_id": shared["message_id"],
        }
        print(f"🔍 [FetchDiscordHistory] Prep result: {prep_result}")
        return prep_result

    async def exec_async(self, prep_res):
        print("📥 [FetchDiscordHistory] Starting exec_async")
        print(f"📥 [FetchDiscordHistory] Prep result received: {prep_res}")
        print(f"📥 [FetchDiscordHistory] Bot instance: {self.bot}")
        print(f"📥 [FetchDiscordHistory] Fetching channel {prep_res['channel_id']}")

        # Try to get channel from cache first, then fetch if not found
        channel = self.bot.get_channel(prep_res["channel_id"])
        print(f"📥 [FetchDiscordHistory] Channel from cache: {channel}")

        if not channel:
            try:
                print(
                    "🔍 [FetchDiscordHistory] Channel not in cache, fetching from API..."
                )
                channel = await self.bot.fetch_channel(prep_res["channel_id"])
                print(f"📥 [FetchDiscordHistory] Channel fetched from API: {channel}")
            except discord.NotFound:
                print(
                    f"❌ [FetchDiscordHistory] Channel not found: {prep_res['channel_id']}"
                )
                return []
            except discord.Forbidden:
                print(
                    f"❌ [FetchDiscordHistory] No permission to access channel: {prep_res['channel_id']}"
                )
                return []

        # Handle different channel types
        if hasattr(channel, "name"):
            channel_name = channel.name
        elif isinstance(channel, discord.DMChannel):
            channel_name = "DM"
        else:
            channel_name = "Unknown"

        print(
            f"📥 [FetchDiscordHistory] Channel found: {channel_name} (ID: {channel.id})"
        )

        try:
            print(
                f"📨 [FetchDiscordHistory] Fetching target message {prep_res['message_id']}"
            )
            target = await channel.fetch_message(prep_res["message_id"])
            print(
                f"📨 [FetchDiscordHistory] Target message found: {target.id} by {target.author}"
            )
            print(
                f"📨 [FetchDiscordHistory] Target message content preview: {target.content[:100]}..."
            )

            print(
                f"📜 [FetchDiscordHistory] Fetching {self.history_limit} messages before target"
            )
            msgs = [
                m
                async for m in channel.history(
                    limit=self.history_limit, before=target, oldest_first=False
                )
            ]

            print(
                f"🔍 [FetchDiscordHistory] Fetched {len(msgs)} messages, checking for [new chat] marker"
            )

            # Look for "[new chat] ---" marker and cut off everything before it (including the marker)
            for i, msg in enumerate(msgs):
                if "[new chat] ---" in msg.content:
                    # Keep only messages from index 0 to i (excluding the marker and everything before it)
                    msgs = msgs[:i]
                    print(
                        f"✂️ [FetchDiscordHistory] Found [new chat] marker, cut history to {len(msgs)} messages (everything before and including marker removed)"
                    )
                    break

            # Reverse to get chronological order (oldest to newest)
            msgs.reverse()
            print(
                f"✅ [FetchDiscordHistory] Successfully processed {len(msgs)} messages"
            )

            # Extract table attachments and their content
            table_content_map = await self._extract_table_attachments(msgs)

            # Debug: show message IDs and authors
            for i, msg in enumerate(msgs):
                print(
                    f"📜 [FetchDiscordHistory] Message {i + 1}: {msg.id} by {msg.author} - {msg.content[:50]}..."
                )

            return {"messages": msgs, "table_map": table_content_map}
        except discord.NotFound as e:
            print(f"❌ [FetchDiscordHistory] Message/Channel not found: {e}")
            return None
        except discord.Forbidden as e:
            print(f"❌ [FetchDiscordHistory] Access forbidden: {e}")
            return None
        except discord.HTTPException as e:
            print(f"❌ [FetchDiscordHistory] HTTP error: {e}")
            return None
        except Exception as e:
            print(f"❌ [FetchDiscordHistory] Unexpected error: {type(e).__name__}: {e}")
            return None

    async def _extract_table_attachments(self, msgs):
        """Extracts table content from attachments and returns a map."""
        print(
            f"🔄 [FetchDiscordHistory] Extracting table attachments from {len(msgs)} messages"
        )
        table_content_map = {}

        for msg in msgs:
            if not msg.attachments:
                continue

            for attachment in msg.attachments:
                if attachment.filename.startswith(
                    "daia_replaced_table_"
                ) and attachment.filename.endswith(".md"):
                    # Extract message_id and count from filename: daia_replaced_table_{message_id}_{count}.md
                    filename_parts = attachment.filename.replace(".md", "").split("_")
                    if len(filename_parts) >= 5:
                        message_id_part = filename_parts[3]
                        count_part = filename_parts[4]

                        if message_id_part.isdigit() and count_part.isdigit():
                            attachment_key = f"{message_id_part}_{count_part}"
                            print(
                                f"📥 [FetchDiscordHistory] Found table attachment: {attachment.filename} with key {attachment_key}"
                            )

                            try:
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(attachment.url) as response:
                                        if response.status == 200:
                                            table_content = await response.text()
                                            table_content_map[attachment_key] = (
                                                table_content
                                            )
                                            print(
                                                f"✅ [FetchDiscordHistory] Downloaded and stored table content for key {attachment_key} ({len(table_content)} chars)"
                                            )
                                        else:
                                            print(
                                                f"❌ [FetchDiscordHistory] Failed to download attachment {attachment.filename}: HTTP {response.status}"
                                            )
                            except Exception as e:
                                print(
                                    f"❌ [FetchDiscordHistory] Error downloading attachment {attachment.filename}: {e}"
                                )

        print(
            f"✅ [FetchDiscordHistory] Completed extracting table attachments, found {len(table_content_map)} tables."
        )
        return table_content_map

    async def post_async(self, shared, prep_res, exec_res):
        print("🔄 [FetchDiscordHistory] Starting post_async")

        if exec_res is None:
            print("❌ [FetchDiscordHistory] exec_res is None, setting result to failed")
            return "failed"

        print(
            f"🔄 [FetchDiscordHistory] Exec result contains {len(exec_res.get('messages', []))} messages and {len(exec_res.get('table_map', {}))} table mappings."
        )

        shared["message_history"] = exec_res.get("messages", [])
        shared["table_content_map"] = exec_res.get("table_map", {})

        # Consider empty list as success (no history is valid), only None/error as failed
        result = "success"

        print(
            "🔄 [FetchDiscordHistory] Updated shared data with message_history and table_content_map"
        )
        print(f"🔄 [FetchDiscordHistory] Shared keys now: {list(shared.keys())}")
        print(f"🔄 [FetchDiscordHistory] Post-processing complete, result: {result}")
        return result
