"""
Discord response sending node for the async flow pipeline.
"""

import os

import discord
from pocketflow import AsyncNode

from utils.discord_helpers import split_message


class SendDiscordResponse(AsyncNode):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

    async def prep_async(self, shared):
        # Use text without tables if available, otherwise use original response
        response_text = shared.get("response_without_tables") or shared.get(
            "llm_response", "No response generated"
        )
        table_images = shared.get("table_images", [])
        extracted_tables_files = shared.get("extracted_tables_files", [])

        print(
            f"� [SenndDiscordResponse] Preparing to send response to channel {shared['channel_id']}"
        )
        print(f"� [SenndDiscordResponse] Response preview: {response_text[:100]}...")
        print(f"🖼️ [SendDiscordResponse] Table images to send: {len(table_images)}")
        print(
            f"📋 [SendDiscordResponse] Table files to send: {len(extracted_tables_files)}"
        )

        return {
            "channel_id": shared["channel_id"],
            "message_id": shared.get(
                "message_id"
            ),  # Add original message ID for replies
            "response_text": response_text,
            "table_images": table_images,
            "extracted_tables_files": extracted_tables_files,
        }

    async def exec_async(self, prep_res):
        print(f"🔍 [SendDiscordResponse] Getting channel {prep_res['channel_id']}")
        # Try to get channel from cache first, then fetch if not found
        channel = self.bot.get_channel(prep_res["channel_id"])

        if not channel:
            try:
                print(
                    "🔍 [SendDiscordResponse] Channel not in cache, fetching from API..."
                )
                channel = await self.bot.fetch_channel(prep_res["channel_id"])
            except (discord.NotFound, discord.Forbidden) as e:
                print(
                    f"❌ [SendDiscordResponse] Cannot access channel {prep_res['channel_id']}: {e}"
                )
                return False

        if channel:
            try:
                print("📤 [SendDiscordResponse] Sending message to Discord...")

                # Prepare files for table images and table files
                files = []

                # Add table images
                if prep_res["table_images"]:
                    for img_data in prep_res["table_images"]:
                        files.append(
                            discord.File(
                                img_data["buffer"], filename=img_data["filename"]
                            )
                        )
                    print(
                        f"🖼️ [SendDiscordResponse] Prepared {len(prep_res['table_images'])} image attachments"
                    )

                # Add table files from temp folder
                if prep_res["extracted_tables_files"]:
                    for table_file in prep_res["extracted_tables_files"]:
                        # The table_file already includes the temp/ path
                        if os.path.exists(table_file):
                            # Extract just the filename for the attachment
                            filename = os.path.basename(table_file)
                            files.append(discord.File(table_file, filename=filename))
                            print(
                                f"📋 [SendDiscordResponse] Added table file: {filename}"
                            )
                        else:
                            print(
                                f"⚠️ [SendDiscordResponse] Table file not found: {table_file}"
                            )
                    print(
                        f"📋 [SendDiscordResponse] Prepared {len([f for f in prep_res['extracted_tables_files'] if os.path.exists(f)])} table file attachments"
                    )

                print(f"📎 [SendDiscordResponse] Total attachments: {len(files)}")

                # Split message if it's too long
                message_chunks = split_message(prep_res["response_text"])
                print(
                    f"📝 [SendDiscordResponse] Message split into {len(message_chunks)} chunks"
                )

                # Get the original message to reply to, if available
                original_message = None
                if prep_res.get("message_id"):
                    try:
                        original_message = await channel.fetch_message(
                            prep_res["message_id"]
                        )
                    except (discord.NotFound, discord.Forbidden) as e:
                        print(
                            f"⚠️ [SendDiscordResponse] Could not fetch original message {prep_res['message_id']}: {e}"
                        )

                if not message_chunks:
                    # If there is no text but there are files, send them
                    if files:
                        if original_message:
                            await original_message.reply(files=files)
                            print(
                                f"✅ [SendDiscordResponse] Sent {len(files)} files as a reply (no text)."
                            )
                        else:
                            await channel.send(files=files)
                            print(
                                f"✅ [SendDiscordResponse] Sent {len(files)} files (no text)."
                            )
                elif len(message_chunks) == 1:
                    # Single chunk: send as a reply with all files
                    if original_message:
                        await original_message.reply(
                            content=message_chunks[0], files=files
                        )
                        print(
                            f"✅ [SendDiscordResponse] Single chunk with {len(files)} files sent as reply"
                        )
                    else:
                        await channel.send(content=message_chunks[0], files=files)
                        print(
                            f"✅ [SendDiscordResponse] Single chunk with {len(files)} files sent (fallback)"
                        )
                else:
                    # Multiple chunks: reply with the first, send middle, then send last with files
                    # Send first chunk as a reply (no files)
                    if original_message:
                        await original_message.reply(message_chunks[0])
                        print("✅ [SendDiscordResponse] First chunk sent as reply")
                    else:
                        await channel.send(message_chunks[0])
                        print("✅ [SendDiscordResponse] First chunk sent (fallback)")

                    # Send middle chunks (if any)
                    for i, chunk in enumerate(message_chunks[1:-1], 2):
                        await channel.send(chunk)
                        print(
                            f"✅ [SendDiscordResponse] Chunk {i}/{len(message_chunks)} sent"
                        )

                    # Send the last chunk with all the files
                    await channel.send(content=message_chunks[-1], files=files)
                    print(
                        f"✅ [SendDiscordResponse] Last chunk ({len(message_chunks)}/{len(message_chunks)}) with {len(files)} files sent"
                    )

                # Clean up table files after successful send
                if prep_res["extracted_tables_files"]:
                    for table_file in prep_res["extracted_tables_files"]:
                        try:
                            if os.path.exists(table_file):
                                os.remove(table_file)
                                print(
                                    f"🗑️ [SendDiscordResponse] Deleted table file: {table_file}"
                                )
                        except Exception as e:
                            print(
                                f"⚠️ [SendDiscordResponse] Failed to delete table file {table_file}: {e}"
                            )
                    print(
                        f"🧹 [SendDiscordResponse] Cleanup completed for {len(prep_res['extracted_tables_files'])} table files"
                    )

                return True
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"❌ [SendDiscordResponse] Failed to send message: {e}")
                return False

        print(f"❌ [SendDiscordResponse] Channel not found: {prep_res['channel_id']}")
        return False

    async def post_async(self, shared, prep_res, exec_res):
        shared["message_sent"] = exec_res
        result = "sent" if exec_res else "failed"
        print(f"🔄 [SendDiscordResponse] Post-processing complete, result: {result}")
        return result
