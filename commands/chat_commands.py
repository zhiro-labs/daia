"""Chat-related Discord slash commands"""

import discord
from discord.ext import commands


def setup_chat_commands(bot: commands.Bot):
    """Register chat-related slash commands"""

    @bot.tree.command(
        name="newchat", description="Start a new chat session by sending a marker"
    )
    async def newchat(interaction: discord.Interaction):
        """Slash command to send a new chat marker"""
        try:
            await interaction.response.send_message("[new chat] ---", ephemeral=False)
            print(
                f"✅ [newchat] New chat marker sent in {interaction.channel.name if hasattr(interaction.channel, 'name') else 'DM'}"
            )
        except Exception as e:
            print(f"❌ [newchat] Error sending new chat marker: {e}")
            await interaction.response.send_message(
                "Failed to send new chat marker.", ephemeral=True
            )
