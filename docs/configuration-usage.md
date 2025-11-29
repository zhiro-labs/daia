---
layout: default
title: Configuration & Usage
nav_order: 3
---

# Configuration & Usage
{: .no_toc }

Complete guide to configuring and using Daia.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Configuration Files

Daia uses two configuration files:

### Environment Variables (`.env`)

Static configuration and secrets that don't change at runtime.

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token from the Developer Portal | `YOUR_DISCORD_BOT_TOKEN_HERE` |
| `CHAT_MODEL_API_KEY` | Your Google Gemini API key | `AIzaSyD1234567890abcdefghijklmnopqrstuv` |
| `CHAT_MODEL` | The Gemini model to use | `gemini-1.5-flash` or `gemini-1.5-pro` |
| `CHAT_TEMPERATURE` | Controls response randomness (0.0–2.0) | `1.0` |
| `HISTORY_LIMIT` | Maximum number of messages to fetch from history | `50` |
| `CHAT_SYS_PROMPT_PATH` | Path to the system prompt file | `config/chat_sys_prompt.txt` |

#### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ENABLE_CONTEXTUAL_SYSTEM_PROMPT` | Enable user recognition by display name | `off` | `on` (recommended) |
| `CHAT_MODEL_PROVIDER` | LLM provider to use | `gemini` | `gemini` |

### Runtime Configuration (`config/runtime.yml`)

Settings that can be modified while the bot is running.

| Setting | Description | Default | Example |
|---------|-------------|---------|---------|
| `allowed_channels` | List of channel IDs where bot responds without mentions | `[]` | `[123456789, 987654321]` |
| `timezone` | Timezone for bot operations | `UTC` | `America/New_York`, `Europe/London` |
| `discord_activity` | Activity status displayed for the bot | `Surfing` | `Listening to music` |

### Configuration Details

#### CHAT_MODEL

Choose based on your needs:

- **gemini-1.5-flash**: Faster responses, lower cost, good for most use cases
- **gemini-1.5-pro**: More capable, better for complex tasks, higher cost

#### CHAT_TEMPERATURE

Controls the randomness of responses:

- **0.0**: Deterministic, focused responses
- **1.0**: Balanced (recommended)
- **2.0**: More creative and varied responses

#### HISTORY_LIMIT

Number of previous messages to include as context:

- **Lower values (10-20)**: Faster, less context
- **Medium values (30-50)**: Balanced (recommended)
- **Higher values (50-100)**: More context, slower, higher token usage

#### allowed_channels

If set in `config/runtime.yml`, the bot will respond to all messages in these channels without requiring a mention. To find a channel ID:

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click a channel and select "Copy Channel ID"

Example in `config/runtime.yml`:
```yaml
allowed_channels:
  - 1234567890
  - 9876543210
  - 1122334455
```

#### ENABLE_CONTEXTUAL_SYSTEM_PROMPT

When enabled (`on`), the bot will:
- Address users by their Discord display name
- Provide more personalized responses
- Include user context in the system prompt

Recommended setting: `on`

---

## System Prompt Customization

The system prompt defines your bot's personality and behavior. Edit `config/chat_sys_prompt.txt` to customize it.

### Example System Prompts

**Helpful Assistant:**
```
You are Daia, a helpful AI assistant in a Discord server.
You provide clear, accurate information and maintain a friendly, professional tone.
When you don't know something, you admit it rather than making up information.
```

**Casual Friend:**
```
You are Daia, a chill AI friend hanging out in Discord.
You keep things casual and fun, using emojis occasionally 😊
You're knowledgeable but never condescending.
```

**Technical Expert:**
```
You are Daia, a technical AI assistant specializing in programming and technology.
You provide detailed, accurate technical information with code examples when relevant.
You explain complex concepts clearly and concisely.
```

### Best Practices

- Keep it concise (2-5 sentences)
- Define the bot's role and personality
- Set expectations for response style
- Include any specific guidelines or restrictions

---

## Usage Guide

### Starting a Conversation

There are three ways to interact with Daia:

#### 1. In Allowed Channels

If you've configured `allowed_channels` in `config/runtime.yml`, simply type your message:

```
What's the weather like today?
```

#### 2. Mention the Bot

In any channel where the bot has access:

```
@Daia what's the capital of France?
```

#### 3. Direct Message

Send the bot a DM for private conversations:

```
Can you help me with something?
```

### Continuing Conversations

Daia remembers recent message history (up to `HISTORY_LIMIT`). You can continue the conversation naturally:

```
You: What's Python?
Daia: Python is a high-level programming language...

You: What's it used for?
Daia: Python is commonly used for...
```

### Starting Fresh

Use the `/newchat` slash command to clear the conversation history and start fresh:

```
/newchat
```

This is useful when:
- Switching topics
- The bot seems confused by previous context
- You want to reset the conversation

### Managing Allowed Channels

Administrators can dynamically manage which channels the bot responds to without being mentioned:

#### `/addchannel`
Add the current channel to the allowed list:

```
/addchannel
```

After running this command, the bot will respond to all messages in this channel without requiring a mention.

#### `/removechannel`
Remove the current channel from the allowed list:

```
/removechannel
```

After running this command, users must mention the bot to get a response in this channel.

#### `/listchannels`
View all channels currently in the allowed list:

```
/listchannels
```

This shows all channels where the bot will respond automatically, along with their channel IDs.

**Note**: These commands require Administrator permissions and only affect runtime behavior. Changes are saved to `config/runtime.yml` and persist across bot restarts.

---

## Features in Detail

### Markdown Table Rendering

When Daia's response contains a markdown table, it's automatically rendered as an image.

**Example:**

```
You: Show me a comparison of programming languages

Daia: Here's a comparison:

| Language | Type | Use Case |
|----------|------|----------|
| Python | Interpreted | Data Science, Web |
| JavaScript | Interpreted | Web Development |
| Rust | Compiled | Systems Programming |

[Image of rendered table]
```

**Supported Languages:**
- English
- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)
- Japanese (日本語)
- Korean (한국어)

The rendering uses Noto Sans CJK fonts for proper display of all characters.

### Smart Message Chunking

Discord has a 2000 character limit per message. Daia automatically splits long responses while preserving formatting:

- Code blocks stay intact
- Lists aren't broken mid-item
- Markdown formatting is preserved
- Each chunk is sent as a separate message

### Google Search Integration

Daia can automatically search the web when needed:

```
You: What's the latest version of Python?
Daia: [Searches Google] The latest version is Python 3.12...
```

This happens automatically when:
- You ask about current events
- You request up-to-date information
- The bot determines a search would be helpful

### User Recognition

With `ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on`, Daia addresses users by their display name:

```
You: Hello!
Daia: Hi John! How can I help you today?
```

This creates a more personalized experience.

---

## Advanced Configuration

### Multiple Servers

You can use the same bot in multiple servers. Each server maintains its own conversation history per channel.

### Channel-Specific Behavior

To restrict the bot to specific channels:

1. Set `allowed_channels` in `config/runtime.yml` to only the channels where you want automatic responses
2. In other channels, users must mention the bot
3. Use Discord's permission system to prevent the bot from seeing certain channels

### Rate Limiting

Be aware of API rate limits:

- **Discord**: 50 requests per second per bot
- **Gemini**: Varies by tier (check your quota in Google AI Studio)

If you hit rate limits:
- Reduce `HISTORY_LIMIT` to send fewer tokens per request
- Implement cooldowns between messages (requires code modification)
- Upgrade your Gemini API tier

### Performance Tuning

For better performance:

- Use `gemini-1.5-flash` instead of `gemini-1.5-pro`
- Lower `HISTORY_LIMIT` to reduce context size
- Reduce `CHAT_TEMPERATURE` for more consistent responses

---

## Common Use Cases

### Community Support Bot

`.env`:
```bash
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=30
```

`config/runtime.yml`:
```yaml
allowed_channels:
  - support-channel-id
```

System prompt:
```
You are a support assistant for [Your Community].
Help users with common questions about [your topic].
Be patient and friendly. If you don't know something, direct users to the documentation.
```

### Personal Assistant

`.env`:
```bash
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=50
```

`config/runtime.yml`:
```yaml
allowed_channels: []  # Leave empty, require mentions
```

System prompt:
```
You are a personal AI assistant.
Help with research, brainstorming, and answering questions.
Provide detailed, thoughtful responses.
```

### Multilingual Server

```bash
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=40
```

System prompt:
```
You are a multilingual AI assistant.
Respond in the same language the user uses.
Support English, Chinese, Japanese, and Korean.
```

---

## Troubleshooting

### Bot responds to every message

**Issue**: Bot is too chatty in channels.

**Solution**: Remove the channel from `allowed_channels` in `config/runtime.yml` so users must mention the bot.

### Bot doesn't remember context

**Issue**: Bot seems to forget previous messages.

**Solution**: Increase `HISTORY_LIMIT` in your `.env` file.

### Responses are too random/inconsistent

**Issue**: Bot gives different answers to the same question.

**Solution**: Lower `CHAT_TEMPERATURE` (try 0.5 or 0.7).

### Tables not rendering

**Issue**: Tables appear as text instead of images.

**Solution**:
- Check that fonts were downloaded (check logs on first run)
- Verify the bot has "Attach Files" permission
- Check for errors in the console output

---

## Next Steps

- Learn about [Development](development.html) to customize Daia
- Explore the [Project Structure](project-structure.html)
- Check out [PocketFlow documentation](https://github.com/The-Pocket/PocketFlow) for advanced workflows
