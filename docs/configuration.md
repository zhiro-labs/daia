---
layout: default
title: Configuration
nav_order: 3
---

# Configuration

Daia uses two configuration files:

## Environment Variables (`.env`)

These are set in a `.env` file in the project root:

- `DISCORD_BOT_TOKEN`: Your Discord bot token. **(Required)**
- `CHAT_MODEL_API_KEY`: Your Google Gemini API key. **(Required)**
- `CHAT_MODEL`: The Gemini model to use (e.g., "gemini-1.5-flash", "gemini-1.5-pro"). **(Required)**
- `CHAT_TEMPERATURE`: Controls the randomness of Gemini's responses (range: 0.0–2.0). **(Required)**
- `CHAT_SYS_PROMPT_PATH`: The path to the system prompt file. **(Required)**
- `ENABLE_CONTEXTUAL_SYSTEM_PROMPT`: Set to `on` to enable the contextual system prompt, which allows the bot to recognize and address users by their display name. The recommended setting is `on` (as set in `.env.example`). If the variable is not set, it defaults to `off`.
- `CHAT_MODEL_PROVIDER`: The LLM provider to use. Currently supports `gemini`. Defaults to `gemini`.

## Runtime Configuration (`config/runtime.yml`)

These settings can be modified at runtime and are stored in `config/runtime.yml`:

- `allowed_channels`: A list of channel IDs where the bot is allowed to respond without being mentioned. If empty, the bot will only respond to direct messages and mentions.
- `allowed_users`: A list of user IDs allowed to DM the bot.
- `timezone`: The timezone for bot operations (e.g., "America/New_York", "Europe/London", "Asia/Tokyo"). Defaults to "UTC".
- `discord_activity`: The activity status displayed for the bot (e.g., "Surfing", "Listening to music").
- `history_limit`: The maximum number of messages to fetch from the channel history. Defaults to 12. Can be changed via `/sethistorylimit` command.
