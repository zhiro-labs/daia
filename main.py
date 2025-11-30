import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pocketflow import AsyncFlow

from nodes.contextual_system_prompt import ContextualSystemPrompt
from nodes.fetch_history import FetchDiscordHistory
from nodes.llm_chat import LLMChat
from nodes.process_history import ProcessMessageHistory
from nodes.send_response import SendDiscordResponse
from nodes.table_extractor import MarkdownTableExtractor
from nodes.table_renderer import TableImageRenderer
from utils import (
    check_font_exists,
    create_message_data,
    download_noto_font,
    env_onoff_to_bool,
    runtime_config,
    validate_message_data_types,
)

# Load environment variables at module level
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# Use runtime config for dynamic values (can be changed via Discord commands)
DISCORD_BOT_ACTIVITY = runtime_config.discord_activity
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT"))

CHAT_MODEL_API_KEY = os.getenv("CHAT_MODEL_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")
CHAT_TEMPERATURE = os.getenv("CHAT_TEMPERATURE")
CHAT_SYS_PROMPT_PATH = os.getenv("CHAT_SYS_PROMPT_PATH")
ENABLE_CONTEXTUAL_SYSTEM_PROMPT = env_onoff_to_bool(
    os.getenv("ENABLE_CONTEXTUAL_SYSTEM_PROMPT")
)
CHAT_MODEL_PROVIDER = os.getenv("CHAT_MODEL_PROVIDER", "gemini")  # Default to gemini


genai_client = genai.Client(api_key=CHAT_MODEL_API_KEY)
with open(CHAT_SYS_PROMPT_PATH, encoding="utf-8") as file:
    genai_chat_system_prompt = file.read()
genai_tools = types.Tool(google_search=types.GoogleSearch())

# Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Read message content (required for Discord API v2+)
intents.members = (
    True  # Read member information (needs to be enabled in Discord Developer Portal)
)
intents.guilds = True  # Default is True, but explicitly written for clarity

custom_activity = discord.CustomActivity(
    name=DISCORD_BOT_ACTIVITY
)  # Or any status message you want to display

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    activity=custom_activity,
    status=discord.Status.online,
)


if not check_font_exists():
    print("🔤 Downloading Noto Sans CJK fonts for markdown table image rendering...")
    print("� This may take a few minutes depending on your connection (~100MB)")
    try:
        download_noto_font()
        print("✅ Font download completed successfully!")
    except Exception as e:
        print(f"❌ Font download failed: {e}")
        print("⚠️  Bot will continue but table rendering may not work properly")
        print("💡 You can try running 'uv run download_fonts.py' later")


async def create_message_flow():
    print("🏗️ [create_message_flow] Creating flow nodes...")
    # Create nodes
    fetch_history = FetchDiscordHistory(bot, HISTORY_LIMIT)
    process_history = ProcessMessageHistory()
    contextual_system_prompt = ContextualSystemPrompt(
        ENABLE_CONTEXTUAL_SYSTEM_PROMPT, genai_chat_system_prompt, HISTORY_LIMIT
    )
    llm_chat = LLMChat(
        genai_client,
        CHAT_MODEL,
        CHAT_TEMPERATURE,
        genai_tools,
        provider=CHAT_MODEL_PROVIDER,
    )
    table_extractor = MarkdownTableExtractor()
    table_renderer = TableImageRenderer()
    send_response = SendDiscordResponse(bot)

    print("🔗 [create_message_flow] Setting up transitions...")
    # Define transitions
    fetch_history - "success" >> process_history
    process_history - "processed" >> contextual_system_prompt
    contextual_system_prompt - "success" >> llm_chat
    llm_chat - "success" >> table_extractor
    table_extractor - "tables_found" >> table_renderer
    table_extractor - "no_tables" >> send_response
    table_renderer - "images_rendered" >> send_response
    table_renderer - "no_images" >> send_response
    fetch_history - "failed" >> send_response  # Skip to response with error handling

    # Create async flow
    flow = AsyncFlow(start=fetch_history)
    print("✅ [create_message_flow] Flow created successfully")
    return flow


@bot.event
async def on_ready():
    print(f"🚀 {bot.user} has connected to Discord!")
    print(f"🤖 Bot ID: {bot.user.id}")
    print(f"🔧 Connected to {len(bot.guilds)} guilds")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


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
        was_added = runtime_config.add_channel(channel_id, server_name, channel_name)

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
    name="removechannel", description="Remove current channel from bot's allowed list"
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
            print(f"✅ [removechannel] Removed channel {channel_id} from allowed list")
        else:
            await interaction.response.send_message(
                f"ℹ️ {interaction.channel.mention} was not in the allowed list",
                ephemeral=True,
            )
            print(f"ℹ️ [removechannel] Channel {channel_id} not found in allowed list")
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
                    channel_mentions.append(f"• {channel.mention} (ID: {channel_id})")

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
            print(f"✅ [adduser] Added user {user_id} ({user.name}) to allowed list")
        else:
            await interaction.response.send_message(
                f"ℹ️ {user.mention} is already in the allowed DM list",
                ephemeral=True,
            )
            print(f"ℹ️ [adduser] User {user_id} ({user.name}) already in allowed list")
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


@bot.tree.command(name="listusers", description="List all users allowed to DM the bot")
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


@bot.event
async def on_message(message: discord.Message):
    """Handle received messages with proper type validation"""
    print(
        f"📨 [on_message] Received message from {message.author.display_name} in #{message.channel.name if hasattr(message.channel, 'name') else 'DM'}"
    )
    print(f"📝 [on_message] Message content: {message.content[:100]}...")

    # Ignore bot's own messages
    if message.author == bot.user:
        print("🚫 [on_message] Ignoring own message")
        return

    # Only respond to messages that mention the bot, are in allowed channels, or are from allowed DM users
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_allowed_dm_user = message.author.id in runtime_config.allowed_users
    is_in_allowed_channel = message.channel.id in runtime_config.allowed_channels
    is_mentioned = bot.user.mentioned_in(message)

    # For DMs, user must be in allowed list regardless of mention
    # For channels, respond if mentioned or in allowed channel
    should_respond = (is_dm and is_allowed_dm_user) or (
        not is_dm and (is_mentioned or is_in_allowed_channel)
    )

    print(
        f"🔍 [on_message] Is DM: {is_dm}, Is allowed DM user: {is_allowed_dm_user}, Is in allowed channel: {is_in_allowed_channel}, Bot mentioned: {is_mentioned}, Should respond: {should_respond}"
    )

    if not should_respond:
        print("🚫 [on_message] Ignoring message - does not meet response criteria")
        return

    print("✅ [on_message] Processing message...")

    # Show typing indicator while processing
    async with message.channel.typing():
        try:
            # Prepare shared data with proper type validation
            message_data = create_message_data(message, bot.user.id)

            print("🔄 [on_message] Message data prepared:")
            print(
                f"  👤 Author: {message_data['author_name']} (ID: {message_data['author_id']})"
            )
            print(f"  �a Channel ID: {message_data['channel_id']}")
            print(f"  🆔 Message ID: {message_data['message_id']}")
            print(
                f"  📊 Data types validated: {validate_message_data_types(message_data)}"
            )

            # Create and run flow
            print("🏗️ [on_message] Creating message flow...")
            flow = await create_message_flow()
            print("▶️ [on_message] Running flow...")
            await flow.run_async(message_data)
            print("✅ [on_message] Flow completed successfully")

        except Exception as e:
            print(f"❌ [on_message] Error processing message: {e}")
            import traceback

            print("🔍 [on_message] Full traceback:")
            traceback.print_exc()
            try:
                await message.channel.send(
                    f"Sorry, an error occurred while processing your message. Error processing message: {e}"
                )
            except Exception as send_error:
                print(f"❌ [on_message] Failed to send error message: {send_error}")


def main():
    print("🚀 Hello from daia!")
    print(f"🔑 Discord token loaded: {'✅' if DISCORD_BOT_TOKEN else '❌'}")
    print(f"🔑 Gemini API key loaded: {'✅' if CHAT_MODEL_API_KEY else '❌'}")
    print(f"🤖 Chat model: {CHAT_MODEL}")
    print(f"🌡️ Chat temperature: {CHAT_TEMPERATURE}")
    print(f"📄 Chat system prompt path: {CHAT_SYS_PROMPT_PATH}")
    print(f"🔌 LLM Provider: {CHAT_MODEL_PROVIDER}")
    print(f"🔌 Contextual system prompt: {ENABLE_CONTEXTUAL_SYSTEM_PROMPT}")
    print("🔌 Starting Discord bot...")
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
