---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started

## Prerequisites

- A Discord Bot Token. You can follow the official guide to create one: [Discord Developer Documentation](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).
- An API key for your chosen LLM provider:
  - Google Gemini: [Google AI Studio](https://aistudio.google.com/apikey)
  - OpenAI: [OpenAI Platform](https://platform.openai.com/api-keys)
  - Anthropic: [Anthropic Console](https://console.anthropic.com/)
  - Other providers: See [any-llm supported providers](https://mozilla-ai.github.io/any-llm/providers/)

## Environment

This project requires Python 3.12+. `uv` will gracefully handle the Python version requirement, create a virtual environment, and manage all project dependencies for you.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zhiro-labs/daia.git
   cd daia
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

   > ℹ️ **Note:**
   > If you don't have `uv` installed, you can follow the official installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

3. **Configure your environment and system prompt:**

   - Copy the example files to create your own configuration:
     ```bash
     cp .env.example .env
     cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
     cp config/runtime.yml.example config/runtime.yml
     ```
   - Edit the `.env` file to add your Discord bot token and Gemini API key.
   - Edit `config/chat_sys_prompt.txt` to customize the bot's personality and instructions.
   - Edit `config/runtime.yml` to configure runtime settings and behavior.

4. **Run the bot:**
   ```bash
   uv run main.py
   ```
   > ℹ️ **Note:**
   > On first run, the bot will automatically download Noto CJK fonts (~100MB) for high-quality table image rendering. This may take a few minutes depending on your internet connection.

## Discord Application Permissions and Intents

For the bot to function correctly, you need to configure its permissions and intents in the [Discord Developer Portal](https://discord.com/developers/).

### Privileged Gateway Intents

Navigate to your bot's settings in the Discord Developer Portal and enable the following privileged gateway intents:

- **Server Members Intent**: Required for the bot to recognize and address users by their display name.
- **Message Content Intent**: Required for the bot to read message content.

### Bot Permissions

When inviting the bot to your server, ensure it has the following permissions:

- **General Permissions**
  - View Channels
- **Text Permissions**
  - Send Messages
  - Attach Files
  - Read Message History
