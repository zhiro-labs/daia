---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started
{: .no_toc }

This guide will walk you through setting up Daia from scratch.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Prerequisites

Before you begin, make sure you have:

### 1. Discord Bot Token

You'll need to create a Discord application and bot:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the "Token" section, click "Reset Token" and copy it (you'll need this later)

For detailed instructions, see the [Discord Developer Documentation](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).

### 2. Google Gemini API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey):

1. Sign in with your Google account
2. Click "Get API Key"
3. Create a new API key or use an existing one
4. Copy the key (you'll need this later)

### 3. Python Environment

This project requires **Python 3.12 or higher**. We use `uv` for dependency management, which will automatically handle the Python version requirement and create a virtual environment for you.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/zhiro-labs/daia.git
cd daia
```

### Step 2: Install uv (if needed)

If you don't have `uv` installed, follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Quick install options:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv
```

### Step 3: Install Dependencies

```bash
uv sync
```

This command will:
- Create a virtual environment
- Install all required dependencies
- Set up the project for development

---

## Configuration

### Step 1: Create Configuration Files

Copy the example files to create your own configuration:

```bash
cp .env.example .env
cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
```

### Step 2: Edit Environment Variables

Open the `.env` file in your favorite text editor and fill in the required values:

```bash
# Required
DISCORD_BOT_TOKEN=your_discord_bot_token_here
CHAT_MODEL_API_KEY=your_gemini_api_key_here
CHAT_MODEL=gemini-1.5-flash
CHAT_TEMPERATURE=1.0
HISTORY_LIMIT=50
CHAT_SYS_PROMPT_PATH=config/chat_sys_prompt.txt

# Optional
DISCORD_BOT_ACTIVITY=Chatting with friends
ALLOWED_CHANNELS=123456789,987654321
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
CHAT_MODEL_PROVIDER=gemini
```

See the [Configuration Reference](configuration-usage.html#environment-variables) for detailed explanations of each variable.

### Step 3: Customize System Prompt

Edit `config/chat_sys_prompt.txt` to customize your bot's personality and behavior. This file contains the instructions that guide how Daia responds to users.

Example:
```
You are Daia, a helpful and friendly AI assistant in a Discord server.
You provide clear, concise answers and maintain a casual, approachable tone.
When users ask questions, you provide accurate information and cite sources when possible.
```

---

## Discord Bot Setup

### Step 1: Enable Privileged Gateway Intents

In the [Discord Developer Portal](https://discord.com/developers/applications):

1. Select your application
2. Go to the "Bot" section
3. Scroll down to "Privileged Gateway Intents"
4. Enable the following:
   - **Server Members Intent** (required for user recognition)
   - **Message Content Intent** (required to read messages)
5. Click "Save Changes"

### Step 2: Configure Bot Permissions

When inviting the bot to your server, ensure it has these permissions:

**General Permissions:**
- View Channels

**Text Permissions:**
- Send Messages
- Attach Files
- Read Message History

### Step 3: Generate Invite Link

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select the permissions listed above
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

---

## Running the Bot

Start Daia with:

```bash
uv run main.py
```

On first run, the bot will automatically download Noto CJK fonts (~100MB) for table rendering. This may take a few minutes depending on your internet connection.

You should see output similar to:

```
Logged in as Daia#1234
Ready to chat!
```

---

## Verification

To verify everything is working:

1. Go to your Discord server
2. Send a message mentioning the bot: `@Daia hello!`
3. The bot should respond with a greeting

If the bot doesn't respond, check the [Troubleshooting](#troubleshooting) section below.

---

## Troubleshooting

### Bot doesn't respond

**Check intents:**
- Ensure "Message Content Intent" is enabled in the Developer Portal
- Restart the bot after enabling intents

**Check permissions:**
- Verify the bot has "View Channels" and "Send Messages" permissions in the channel
- Check the channel's permission overrides

**Check configuration:**
- Verify your `DISCORD_BOT_TOKEN` is correct
- Check that the bot is online in your server's member list

### API Key errors

**Invalid Gemini API key:**
- Verify your `CHAT_MODEL_API_KEY` is correct
- Check that the API key is active in Google AI Studio
- Ensure you haven't exceeded your API quota

### Font download issues

**Slow or failed font download:**
- Check your internet connection
- The fonts are downloaded from GitHub releases
- If download fails, the bot will retry on next startup

### Import or dependency errors

**Module not found:**
```bash
# Reinstall dependencies
uv sync --reinstall
```

**Python version issues:**
- Ensure you have Python 3.12 or higher
- `uv` should handle this automatically, but you can check with `python --version`

---

## Next Steps

Now that Daia is running, you can:

- Learn about [Configuration & Usage](configuration-usage.html)
- Explore [Development](development.html) if you want to contribute
- Check out the [Project Structure](project-structure.html) to understand the codebase

---

## Getting Help

If you encounter issues not covered here:

- Check the [GitHub Issues](https://github.com/zhiro-labs/daia/issues)
- Start a [Discussion](https://github.com/zhiro-labs/daia/discussions)
- Review the [Discord Developer Documentation](https://discord.com/developers/docs)
