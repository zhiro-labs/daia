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
    validate_message_data_types,
)

# Load environment variables at module level
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_BOT_ACTIVITY = os.getenv("DISCORD_BOT_ACTIVITY")
# Parse comma-separated channel IDs from environment variable into a set of integers
ALLOWED_CHANNELS = {
    int(stripped)
    for ch in os.getenv("ALLOWED_CHANNELS", "").split(",")
    if (stripped := ch.strip()) and stripped.isdigit()
}
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")
CHAT_TEMPERATURE = os.getenv("CHAT_TEMPERATURE")
CHAT_SYS_PROMPT_PATH = os.getenv("CHAT_SYS_PROMPT_PATH")
ENABLE_CONTEXTUAL_SYSTEM_PROMPT = env_onoff_to_bool(
    os.getenv("ENABLE_CONTEXTUAL_SYSTEM_PROMPT")
)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # Default to gemini


genai_client = genai.Client(api_key=GEMINI_API_KEY)
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
        genai_client, CHAT_MODEL, CHAT_TEMPERATURE, genai_tools, provider=LLM_PROVIDER
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

    # Only respond to messages that mention the bot or are direct messages
    is_mentioned = bot.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_in_allowed_channel = message.channel.id in ALLOWED_CHANNELS

    print(
        f"🔍 [on_message] Bot mentioned: {is_mentioned}, Is DM: {is_dm}, Is in allowed channel: {is_in_allowed_channel}"
    )

    if not (is_mentioned or is_dm or is_in_allowed_channel):
        print(
            "🚫 [on_message] Not mentioned, not DM, and not in allowed channel - ignoring"
        )
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
    print(f"🔑 Gemini API key loaded: {'✅' if GEMINI_API_KEY else '❌'}")
    print(f"🤖 Chat model: {CHAT_MODEL}")
    print(f"🌡️ Chat temperature: {CHAT_TEMPERATURE}")
    print(f"📄 Chat system prompt path: {CHAT_SYS_PROMPT_PATH}")
    print(f"🔌 LLM Provider: {LLM_PROVIDER}")
    print(f"🔌 Contextual system prompt: {ENABLE_CONTEXTUAL_SYSTEM_PROMPT}")
    print("🔌 Starting Discord bot...")
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
