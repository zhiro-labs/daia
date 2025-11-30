"""Admin-related Discord slash commands"""

from zoneinfo import available_timezones

import discord
from discord.ext import commands


def setup_admin_commands(bot: commands.Bot, runtime_config):
    """Register admin-related slash commands"""

    @bot.tree.command(
        name="addchannel", description="Add current channel to bot's allowed list"
    )
    @commands.has_permissions(administrator=True)
    async def addchannel(interaction: discord.Interaction):
        """Slash command to add current channel to allowed channels"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            channel_id = interaction.channel.id
            server_name = interaction.guild.name if interaction.guild else "DM"
            channel_name = (
                interaction.channel.name
                if hasattr(interaction.channel, "name")
                else "Unknown"
            )
            was_added = runtime_config.add_channel(
                channel_id, server_name, channel_name
            )

            if was_added:
                await interaction.response.send_message(
                    f"✅ Added {interaction.channel.mention} to allowed channels list",
                    ephemeral=True,
                )
                print(f"✅ [addchannel] Added channel {channel_id} to allowed list")
            else:
                await interaction.response.send_message(
                    f"ℹ️ {interaction.channel.mention} is already in the allowed list",
                    ephemeral=True,
                )
                print(f"ℹ️ [addchannel] Channel {channel_id} already in allowed list")
        except Exception as e:
            print(f"❌ [addchannel] Error adding channel: {e}")
            await interaction.response.send_message(
                "Failed to add channel to allowed list.", ephemeral=True
            )

    @bot.tree.command(
        name="removechannel",
        description="Remove current channel from bot's allowed list",
    )
    @commands.has_permissions(administrator=True)
    async def removechannel(interaction: discord.Interaction):
        """Slash command to remove current channel from allowed channels"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            channel_id = interaction.channel.id
            was_removed = runtime_config.remove_channel(channel_id)

            if was_removed:
                await interaction.response.send_message(
                    f"✅ Removed {interaction.channel.mention} from allowed channels list",
                    ephemeral=True,
                )
                print(
                    f"✅ [removechannel] Removed channel {channel_id} from allowed list"
                )
            else:
                await interaction.response.send_message(
                    f"ℹ️ {interaction.channel.mention} was not in the allowed list",
                    ephemeral=True,
                )
                print(
                    f"ℹ️ [removechannel] Channel {channel_id} not found in allowed list"
                )
        except Exception as e:
            print(f"❌ [removechannel] Error removing channel: {e}")
            await interaction.response.send_message(
                "Failed to remove channel from allowed list.", ephemeral=True
            )

    @bot.tree.command(
        name="listchannels",
        description="List all channels where bot is allowed in this server",
    )
    @commands.has_permissions(administrator=True)
    async def listchannels(interaction: discord.Interaction):
        """Slash command to list all allowed channels in the current server"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            allowed = runtime_config.allowed_channels
            if not allowed:
                await interaction.response.send_message(
                    "ℹ️ No channels in allowed list. Bot will only respond to mentions.",
                    ephemeral=True,
                )
            else:
                # Filter channels to only show those from the current server
                channel_mentions = []
                for channel_id in allowed:
                    channel = bot.get_channel(channel_id)
                    if (
                        channel
                        and channel.guild
                        and channel.guild.id == interaction.guild.id
                    ):
                        channel_mentions.append(
                            f"• {channel.mention} (ID: {channel_id})"
                        )

                if not channel_mentions:
                    await interaction.response.send_message(
                        f"ℹ️ No allowed channels in **{interaction.guild.name}**.",
                        ephemeral=True,
                    )
                else:
                    message = (
                        f"**Allowed Channels in {interaction.guild.name}:**\n"
                        + "\n".join(channel_mentions)
                    )
                    await interaction.response.send_message(message, ephemeral=True)
                    print(
                        f"✅ [listchannels] Listed {len(channel_mentions)} allowed channels for guild {interaction.guild.id}"
                    )
        except Exception as e:
            print(f"❌ [listchannels] Error listing channels: {e}")
            await interaction.response.send_message(
                "Failed to list allowed channels.", ephemeral=True
            )

    @bot.tree.command(name="adduser", description="Add a user to bot's allowed DM list")
    @commands.has_permissions(administrator=True)
    async def adduser(interaction: discord.Interaction, user: discord.User):
        """Slash command to add user to allowed DM users"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            user_id = user.id
            username = (
                f"{user.name}#{user.discriminator}"
                if user.discriminator != "0"
                else user.name
            )
            was_added = runtime_config.add_user(user_id, username)

            if was_added:
                await interaction.response.send_message(
                    f"✅ Added {user.mention} to allowed DM users list",
                    ephemeral=True,
                )
                print(
                    f"✅ [adduser] Added user {user_id} ({user.name}) to allowed list"
                )
            else:
                await interaction.response.send_message(
                    f"ℹ️ {user.mention} is already in the allowed DM list",
                    ephemeral=True,
                )
                print(
                    f"ℹ️ [adduser] User {user_id} ({user.name}) already in allowed list"
                )
        except Exception as e:
            print(f"❌ [adduser] Error adding user: {e}")
            await interaction.response.send_message(
                "Failed to add user to allowed DM list.", ephemeral=True
            )

    @bot.tree.command(
        name="removeuser", description="Remove a user from bot's allowed DM list"
    )
    @commands.has_permissions(administrator=True)
    async def removeuser(interaction: discord.Interaction, user: discord.User):
        """Slash command to remove user from allowed DM users"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            user_id = user.id
            was_removed = runtime_config.remove_user(user_id)

            if was_removed:
                await interaction.response.send_message(
                    f"✅ Removed {user.mention} from allowed DM users list",
                    ephemeral=True,
                )
                print(
                    f"✅ [removeuser] Removed user {user_id} ({user.name}) from allowed list"
                )
            else:
                await interaction.response.send_message(
                    f"ℹ️ {user.mention} was not in the allowed DM list",
                    ephemeral=True,
                )
                print(
                    f"ℹ️ [removeuser] User {user_id} ({user.name}) not found in allowed list"
                )
        except Exception as e:
            print(f"❌ [removeuser] Error removing user: {e}")
            await interaction.response.send_message(
                "Failed to remove user from allowed DM list.", ephemeral=True
            )

    @bot.tree.command(
        name="listusers", description="List all users allowed to DM the bot"
    )
    @commands.has_permissions(administrator=True)
    async def listusers(interaction: discord.Interaction):
        """Slash command to list all allowed DM users"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            allowed = runtime_config.allowed_users
            if not allowed:
                await interaction.response.send_message(
                    "ℹ️ No users in allowed DM list.",
                    ephemeral=True,
                )
            else:
                user_mentions = []
                for user_id in allowed:
                    user = await bot.fetch_user(user_id)
                    if user:
                        user_mentions.append(f"• {user.mention} (ID: {user_id})")
                    else:
                        user_mentions.append(f"• Unknown user (ID: {user_id})")

                message = "**Allowed DM Users:**\n" + "\n".join(user_mentions)
                await interaction.response.send_message(message, ephemeral=True)
                print(f"✅ [listusers] Listed {len(allowed)} allowed users")
        except Exception as e:
            print(f"❌ [listusers] Error listing users: {e}")
            await interaction.response.send_message(
                "Failed to list allowed users.", ephemeral=True
            )

    @bot.tree.command(
        name="refreshmetadata",
        description="Refresh all channel and user names in config comments",
    )
    @commands.has_permissions(administrator=True)
    async def refreshmetadata(interaction: discord.Interaction):
        """Slash command to refresh all metadata for channels and users"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            # Defer response since this might take a moment
            await interaction.response.defer(ephemeral=True)

            channel_updates = {}
            user_updates = {}

            # Collect channel metadata
            for channel_id in runtime_config.allowed_channels:
                channel = bot.get_channel(channel_id)
                if channel and hasattr(channel, "guild"):
                    channel_updates[channel_id] = {
                        "server": channel.guild.name,
                        "channel": channel.name,
                    }

            # Collect user metadata
            for user_id in runtime_config.allowed_users:
                try:
                    user = await bot.fetch_user(user_id)
                    if user:
                        username = (
                            f"{user.name}#{user.discriminator}"
                            if user.discriminator != "0"
                            else user.name
                        )
                        user_updates[user_id] = {"username": username}
                except Exception as e:
                    print(f"⚠️ [refreshmetadata] Could not fetch user {user_id}: {e}")

            # Batch update all metadata in one operation
            runtime_config.batch_update_metadata(
                channels=channel_updates if channel_updates else None,
                users=user_updates if user_updates else None,
            )

            await interaction.followup.send(
                f"✅ Refreshed metadata for {len(channel_updates)} channel(s) and {len(user_updates)} user(s)",
                ephemeral=True,
            )
            print(
                f"✅ [refreshmetadata] Updated {len(channel_updates)} channels and {len(user_updates)} users"
            )
        except Exception as e:
            print(f"❌ [refreshmetadata] Error refreshing metadata: {e}")
            try:
                await interaction.followup.send(
                    "Failed to refresh metadata.", ephemeral=True
                )
            except Exception:
                await interaction.response.send_message(
                    "Failed to refresh metadata.", ephemeral=True
                )

    @bot.tree.command(
        name="sethistorylimit",
        description="Set the number of messages to include in conversation history",
    )
    @commands.has_permissions(administrator=True)
    async def sethistorylimit(interaction: discord.Interaction, limit: int):
        """Slash command to set history limit"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            runtime_config.set_history_limit(limit)
            await interaction.response.send_message(
                f"✅ History limit set to {limit} messages",
                ephemeral=True,
            )
            print(f"✅ [sethistorylimit] History limit updated to {limit}")
        except Exception as e:
            print(f"❌ [sethistorylimit] Error setting history limit: {e}")
            await interaction.response.send_message(
                "Failed to set history limit.", ephemeral=True
            )

    @bot.tree.command(
        name="setactivity",
        description="Set the bot's Discord activity status message",
    )
    @commands.has_permissions(administrator=True)
    async def setactivity(interaction: discord.Interaction, activity: str):
        """Slash command to set Discord activity status"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            # Validate activity length
            if len(activity) > 128:
                await interaction.response.send_message(
                    "❌ Activity message is too long (max 128 characters).",
                    ephemeral=True,
                )
                return

            runtime_config.set_discord_activity(activity)

            # Update bot's activity in real-time
            custom_activity = discord.CustomActivity(name=activity)
            await bot.change_presence(
                activity=custom_activity, status=discord.Status.online
            )

            await interaction.response.send_message(
                f"✅ Bot activity updated to: {activity}\n(Will persist after bot restart)",
                ephemeral=True,
            )
            print(f"✅ [setactivity] Activity updated to: {activity}")
        except Exception as e:
            print(f"❌ [setactivity] Error setting activity: {e}")
            await interaction.response.send_message(
                "Failed to set activity status.", ephemeral=True
            )

    async def timezone_autocomplete(
        interaction: discord.Interaction, current: str
    ) -> list[discord.app_commands.Choice[str]]:
        """Autocomplete for timezone selection"""
        # Popular timezones to show when no input
        popular = [
            "UTC",
            "America/New_York",
            "America/Chicago",
            "America/Denver",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Asia/Hong_Kong",
            "Asia/Singapore",
            "Asia/Taipei",
            "Australia/Sydney",
        ]

        if not current:
            # Show popular timezones when no input
            return [discord.app_commands.Choice(name=tz, value=tz) for tz in popular]

        # Filter all timezones based on current input
        timezones = sorted(available_timezones())
        filtered = [tz for tz in timezones if current.lower() in tz.lower()][:25]
        return [discord.app_commands.Choice(name=tz, value=tz) for tz in filtered]

    @bot.tree.command(
        name="settimezone",
        description="Set the bot's timezone for timestamps",
    )
    @discord.app_commands.autocomplete(timezone=timezone_autocomplete)
    @commands.has_permissions(administrator=True)
    async def settimezone(interaction: discord.Interaction, timezone: str):
        """Slash command to set timezone"""
        try:
            # Check if command is used in a server
            if not interaction.guild:
                await interaction.response.send_message(
                    "❌ This command can only be used in a server, not in DMs.",
                    ephemeral=True,
                )
                return

            # Validate timezone
            if timezone not in available_timezones():
                await interaction.response.send_message(
                    f"❌ Invalid timezone: {timezone}",
                    ephemeral=True,
                )
                return

            runtime_config.set_timezone(timezone)
            await interaction.response.send_message(
                f"✅ Timezone set to: {timezone}",
                ephemeral=True,
            )
            print(f"✅ [settimezone] Timezone updated to: {timezone}")
        except Exception as e:
            print(f"❌ [settimezone] Error setting timezone: {e}")
            await interaction.response.send_message(
                "Failed to set timezone.", ephemeral=True
            )
