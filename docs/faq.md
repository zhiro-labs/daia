---
layout: default
title: FAQ
nav_order: 8
---

# Frequently Asked Questions
{: .no_toc }

Common questions and answers about Daia.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## General Questions

### What is Daia?

Daia (Discord AI Agent) is an intelligent Discord bot powered by Google Gemini. It provides conversational AI capabilities with features like markdown table rendering, message history processing, and Google Search integration.

### Is Daia free to use?

Yes, Daia is open source and free to use under the MIT License. However, you'll need your own API keys:
- Discord Bot Token (free)
- Google Gemini API Key (free tier available)

### What makes Daia different from other Discord bots?

Daia offers:
- Advanced table rendering with multilingual support
- Smart message chunking
- Context-aware conversations
- Built on PocketFlow for extensibility
- Easy customization through system prompts

### Can I use Daia in multiple servers?

Yes! The same bot instance can be added to multiple Discord servers. Each server maintains its own conversation history per channel.

---

## Setup and Installation

### What are the system requirements?

- Python 3.12 or higher
- Internet connection for API calls
- ~100MB disk space for fonts
- Discord Bot Token
- Google Gemini API Key

### Do I need coding experience to set up Daia?

Basic command-line knowledge is helpful, but the setup process is straightforward. Follow the [Getting Started](getting-started.html) guide for step-by-step instructions.

### Can I run Daia on a Raspberry Pi?

Yes, as long as it supports Python 3.12+. Performance may vary depending on the model. Consider using `gemini-1.5-flash` for better performance on limited hardware.

### How do I get a Discord Bot Token?

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" section
4. Click "Add Bot" and copy the token

See the [Getting Started](getting-started.html#prerequisites) guide for detailed instructions.

### How do I get a Gemini API Key?

Visit [Google AI Studio](https://aistudio.google.com/apikey), sign in with your Google account, and create an API key. The free tier includes generous quotas for testing and personal use.

### Why does the first run take so long?

On first run, Daia downloads Noto CJK fonts (~100MB) for table rendering. This is a one-time download. Subsequent starts will be much faster.

---

## Configuration

### How do I customize the bot's personality?

Edit the `config/chat_sys_prompt.txt` file. This system prompt defines how the bot behaves and responds. See [Configuration & Usage](configuration-usage.html#system-prompt-customization) for examples.

### Can I make the bot respond without being mentioned?

Yes! Set the `ALLOWED_CHANNELS` environment variable to a comma-separated list of channel IDs where the bot should respond to all messages.

```bash
ALLOWED_CHANNELS=123456789,987654321
```

### How do I change which AI model is used?

Edit the `CHAT_MODEL` variable in your `.env` file:

```bash
# Fast and cost-effective
CHAT_MODEL=gemini-1.5-flash

# More capable
CHAT_MODEL=gemini-1.5-pro
```

### What does CHAT_TEMPERATURE do?

Temperature controls response randomness:
- **0.0-0.5**: Focused, deterministic responses
- **0.5-1.5**: Balanced (1.0 recommended)
- **1.5-2.0**: More creative and varied

### How many messages should HISTORY_LIMIT be?

Recommended values:
- **10-20**: Fast, minimal context
- **30-50**: Balanced (recommended)
- **50-100**: Maximum context, slower

Higher values use more tokens and cost more.

---

## Usage

### How do I talk to the bot?

Three ways:
1. In allowed channels: just type your message
2. Anywhere: mention the bot (`@Daia hello`)
3. Direct message: send a DM to the bot

### Does the bot remember previous messages?

Yes, up to the `HISTORY_LIMIT` you configured. Use `/newchat` to start fresh.

### Can the bot search the internet?

Yes! Daia can automatically use Google Search when it needs up-to-date information. This happens automatically through Gemini's tools.

### Why are tables rendered as images?

Discord's markdown support is limited and doesn't handle complex tables well, especially with CJK characters. Rendering tables as images ensures they display correctly for all users.

### What languages are supported for table rendering?

- English
- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)
- Japanese (日本語)
- Korean (한국어)

And any other language supported by Noto Sans CJK fonts.

### Can the bot process images?

Not yet, but it's on the [roadmap](roadmap.html#image-processing)!

### How do I clear the conversation history?

Use the `/newchat` slash command. This clears the context and starts a fresh conversation.

---

## Troubleshooting

### The bot doesn't respond to my messages

Check:
1. **Message Content Intent** is enabled in Discord Developer Portal
2. Bot has "View Channels" and "Send Messages" permissions
3. Bot is online (check member list)
4. You're either in an allowed channel or mentioning the bot

### I get "Invalid API Key" errors

- Verify your `CHAT_MODEL_API_KEY` in `.env` is correct
- Check the key is active in Google AI Studio
- Ensure you haven't exceeded your API quota

### Tables aren't rendering as images

- Check that fonts downloaded successfully (check console output)
- Verify bot has "Attach Files" permission
- Look for errors in the console

### The bot's responses are cut off

This shouldn't happen as Daia automatically chunks long messages. If it does:
- Check console for errors
- Verify you're running the latest version
- Report the issue on GitHub

### Font download fails

- Check your internet connection
- Fonts are downloaded from GitHub releases
- If it fails, the bot will retry on next startup
- You can manually download fonts to `assets/fonts/`

### The bot is slow to respond

Possible causes:
- High `HISTORY_LIMIT` (try reducing it)
- Using `gemini-1.5-pro` (try `gemini-1.5-flash`)
- API rate limiting
- Network latency

### I'm getting rate limited

- Reduce `HISTORY_LIMIT` to send fewer tokens
- Add delays between requests (requires code modification)
- Check your Gemini API quota
- Consider upgrading your API tier

---

## Features

### Can I use other AI models besides Gemini?

Currently, only Gemini is supported. OpenAI and other providers are on the [roadmap](roadmap.html#openai-support).

### Can the bot remember things long-term?

Not yet. Currently, memory is limited to the conversation history (`HISTORY_LIMIT`). Long-term memory is [planned](roadmap.html#long-term-memory).

### Can I add custom commands?

Yes! You can modify the code to add new slash commands. See the [Development Guide](development.html#adding-new-features) for instructions.

### Does the bot support voice channels?

No, Daia is text-only. Voice support is not currently planned.

### Can the bot moderate my server?

Daia is designed for conversation, not moderation. While you could extend it for moderation tasks, there are better-suited bots for that purpose.

---

## Privacy and Security

### What data does Daia store?

By default, Daia doesn't store any data persistently. Message history is kept in memory only during active conversations. Database support for optional persistence is [planned](roadmap.html#database-support).

### Is my conversation data sent to Google?

Yes, messages are sent to Google Gemini API for processing. Review [Google's privacy policy](https://policies.google.com/privacy) for details on how they handle data.

### Can I self-host Daia?

Yes! Daia is designed to be self-hosted. You run it on your own server with your own API keys.

### Is my API key secure?

Your API key is stored in the `.env` file, which should never be committed to git (it's in `.gitignore`). Keep this file secure and don't share it.

### Can I use Daia in a private server?

Absolutely! Daia works in any Discord server where you have permission to add bots.

---

## Development

### Can I contribute to Daia?

Yes! Contributions are welcome. See the [Development Guide](development.html) for instructions.

### How do I report a bug?

Open an issue on [GitHub Issues](https://github.com/zhiro-labs/daia/issues) with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Console output (if applicable)

### How do I request a feature?

Open a discussion on [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions) or check the [roadmap](roadmap.html) to see if it's already planned.

### What is PocketFlow?

PocketFlow is a workflow framework that Daia is built on. It organizes functionality into modular nodes that can be composed into workflows. Learn more at the [PocketFlow repository](https://github.com/The-Pocket/PocketFlow).

### Can I create plugins for Daia?

The plugin system is not formalized yet, but you can extend Daia by:
- Adding new nodes
- Creating utility functions
- Modifying the workflow

See the [Project Structure](project-structure.html) guide.

---

## Costs

### How much does it cost to run Daia?

Costs depend on usage:
- **Discord Bot**: Free
- **Gemini API**: Free tier available, then pay-per-use
- **Hosting**: Free if running on your own computer, or cloud hosting costs

### What's the Gemini API pricing?

Check [Google's pricing page](https://ai.google.dev/pricing) for current rates. The free tier is generous for personal use.

### How can I reduce API costs?

- Use `gemini-1.5-flash` instead of `gemini-1.5-pro`
- Lower `HISTORY_LIMIT` to send fewer tokens
- Restrict bot to specific channels
- Implement rate limiting

---

## Comparison

### Daia vs ChatGPT Discord bots?

Daia advantages:
- Open source and self-hosted
- Customizable system prompts
- Advanced table rendering
- Built on extensible framework
- No subscription required

### Daia vs other AI Discord bots?

Daia is designed for:
- Developers who want customization
- Communities that need self-hosting
- Users who want multilingual table support
- Projects that need extensibility

---

## Getting Help

### Where can I get help?

- **Documentation**: [zhiro-labs.github.io/daia](https://zhiro-labs.github.io/daia/)
- **GitHub Issues**: [Report bugs](https://github.com/zhiro-labs/daia/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/zhiro-labs/daia/discussions)
- **Discord Developer Docs**: [Discord documentation](https://discord.com/developers/docs)

### How do I stay updated?

- Watch the [GitHub repository](https://github.com/zhiro-labs/daia)
- Check the [roadmap](roadmap.html) for planned features
- Follow release notes for updates

---

## Miscellaneous

### What does "Daia" mean?

Daia stands for "Discord AI Agent". It's also a friendly, easy-to-pronounce name!

### Who created Daia?

Daia is developed by Zhiro Labs and built on the PocketFlow framework by [Zachary Huang](https://github.com/zachary62).

### Can I use Daia commercially?

Yes, under the MIT License. You're free to use, modify, and distribute Daia, including for commercial purposes.

### How can I support the project?

- ⭐ Star the repository on GitHub
- 🐛 Report bugs and issues
- 💡 Suggest features
- 🔧 Contribute code
- 📖 Improve documentation
- 💬 Help others in discussions

---

## Still have questions?

If your question isn't answered here:

1. Check the [full documentation](index.html)
2. Search [GitHub Issues](https://github.com/zhiro-labs/daia/issues)
3. Ask in [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions)
4. Open a new issue if you found a bug
