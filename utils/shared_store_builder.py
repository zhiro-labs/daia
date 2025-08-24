"""
Shared store builder for creating and validating message data structures.
"""

from datetime import datetime
from typing import Any

import discord


def create_message_data(message: discord.Message, bot_user_id: int) -> dict[str, Any]:
    """Create message data with proper type validation"""
    try:
        # Ensure all IDs are integers
        author_id = int(message.author.id)
        channel_id = int(message.channel.id)
        message_id = int(message.id)
        bot_id = int(bot_user_id)

        # Ensure string types
        content = str(message.content) if message.content else ""
        author_name = str(message.author.display_name)

        # Process embed content
        embeds = []
        if message.embeds:
            for embed in message.embeds:
                try:
                    # Convert embed to dictionary format
                    embed_dict = embed.to_dict()
                    embeds.append(embed_dict)
                except Exception as e:
                    print(f"⚠️ [create_message_data] Error processing embed: {e}")

        # Get channel name (if available)
        channel_name = ""
        if hasattr(message.channel, "name") and message.channel.name:
            channel_name = str(message.channel.name)
        elif isinstance(message.channel, discord.DMChannel):
            channel_name = "DM"

        # Get server information (if in a server)
        guild_id = None
        guild_name = ""
        if message.guild:
            guild_id = int(message.guild.id)
            guild_name = str(message.guild.name)

        message_data = {
            # Basic message information
            "content": content,
            "embeds": embeds,
            # User information (ensure integers)
            "author_id": author_id,
            "author_name": author_name,
            # Channel information (ensure integers)
            "channel_id": channel_id,
            "channel_name": channel_name,
            # Message ID (ensure integer)
            "message_id": message_id,
            # Bot information (ensure integer)
            "bot_user_id": bot_id,
            # Server information
            "guild_id": guild_id,
            "guild_name": guild_name,
            # Timestamp
            "timestamp": datetime.now().isoformat(),
            "created_at": message.created_at.isoformat(),
            # Message type information
            "is_dm": isinstance(message.channel, discord.DMChannel),
            "has_embeds": len(embeds) > 0,
            "message_type": str(message.type),
            # Attachment information
            "attachments": [
                {
                    "filename": str(attachment.filename),
                    "url": str(attachment.url),
                    "size": int(attachment.size),
                }
                for attachment in message.attachments
            ]
            if message.attachments
            else [],
        }

        return message_data

    except Exception as e:
        print(f"❌ [create_message_data] Error creating message data: {e}")
        raise


def validate_message_data_types(data: dict[str, Any]) -> bool:
    """Validate the types of key fields in message_data"""
    try:
        # Check integer type fields
        int_fields = ["author_id", "channel_id", "message_id", "bot_user_id"]
        for field in int_fields:
            if field in data and not isinstance(data[field], int):
                print(
                    f"❌ [validate_message_data_types] {field} is not int: {type(data[field])}"
                )
                return False

        # Check optional integer fields
        if data.get("guild_id") is not None and not isinstance(data["guild_id"], int):
            print(
                f"❌ [validate_message_data_types] guild_id is not int: {type(data['guild_id'])}"
            )
            return False

        # Check string type fields
        string_fields = [
            "content",
            "author_name",
            "channel_name",
            "guild_name",
            "timestamp",
        ]
        for field in string_fields:
            if field in data and not isinstance(data[field], str):
                print(
                    f"❌ [validate_message_data_types] {field} is not str: {type(data[field])}"
                )
                return False

        # Check list type fields
        list_fields = ["embeds", "attachments"]
        for field in list_fields:
            if field in data and not isinstance(data[field], list):
                print(
                    f"❌ [validate_message_data_types] {field} is not list: {type(data[field])}"
                )
                return False

        print("✅ [validate_message_data_types] All types validated successfully")
        return True

    except Exception as e:
        print(f"❌ [validate_message_data_types] Validation error: {e}")
        return False
