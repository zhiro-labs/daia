---
layout: default
title: Quick Reference
nav_order: 7
---

# Quick Reference
{: .no_toc }

Quick reference guide for common tasks and configurations.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Installation Commands

```bash
# Clone repository
git clone https://github.com/zhiro-labs/daia.git
cd daia

# Install dependencies
uv sync

# Configure
cp .env.example .env
cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt

# Run
uv run main.py
```

---

## Environment Variables

### Required

```bash
DISCORD_BOT_TOKEN=your_bot_token
CHAT_MODEL_API_KEY=your_gemini_api_key
CHAT_MODEL=gemini-1.5-flash
CHAT_TEMPERATURE=1.0
HISTORY_LIMIT=50
CHAT_SYS_PROMPT_PATH=config/chat_sys_prompt.txt
```

### Optional

```bash
DISCORD_BOT_ACTIVITY=Chatting
ALLOWED_CHANNELS=123456789,987654321
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
CHAT_MODEL_PROVIDER=gemini
```

---

## Discord Setup Checklist

- [ ] Create application in [Discord Developer Portal](https://discord.com/developers/applications)
- [ ] Create bot and copy token
- [ ] Enable **Server Members Intent**
- [ ] Enable **Message Content Intent**
- [ ] Generate invite URL with permissions:
  - View Channels
  - Send Messages
  - Attach Files
  - Read Message History
- [ ] Add bot to server

---

## Usage

### Starting Conversations

```
# In allowed channels
Hello Daia!

# Anywhere else
@Daia what's the weather?

# Direct message
[Send DM to bot]
```

### Slash Commands

```
/newchat - Start a fresh conversation
```

---

## Development Commands

```bash
# Install dev dependencies
uv sync --dev

# Format code
make format

# Lint code
make lint

# Run tests
make test

# Run all CI checks
make ci

# Clean cache files
make clean

# Show all commands
make help
```

---

## Common Issues

### Bot doesn't respond
- Check Message Content Intent is enabled
- Verify bot has permissions in channel
- Check bot is online

### API errors
- Verify API key is correct
- Check API quota in Google AI Studio
- Ensure model name is correct

### Font issues
- Check internet connection
- Wait for download to complete
- Restart bot if download failed

---

## File Locations

```
.env                              # Environment variables
config/chat_sys_prompt.txt        # System prompt
main.py                           # Entry point
nodes/                            # Core functionality
utils/                            # Helper functions
tests/                            # Test suite
```

---

## Model Options

### Gemini Models

```bash
# Fast, cost-effective
CHAT_MODEL=gemini-1.5-flash

# More capable, higher cost
CHAT_MODEL=gemini-1.5-pro
```

### Temperature Settings

```bash
# Deterministic (0.0-0.5)
CHAT_TEMPERATURE=0.3

# Balanced (0.5-1.5)
CHAT_TEMPERATURE=1.0

# Creative (1.5-2.0)
CHAT_TEMPERATURE=1.8
```

---

## Testing

```bash
# Run all tests
make test

# Run specific test
uv run pytest tests/test_file.py

# Run with coverage
uv run pytest --cov=.

# Verbose output
uv run pytest -v
```

---

## Git Workflow

```bash
# Switch to dev branch
git checkout dev

# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/my-feature
```

---

## Useful Links

- [GitHub Repository](https://github.com/zhiro-labs/daia)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Google AI Studio](https://aistudio.google.com/apikey)
- [PocketFlow](https://github.com/The-Pocket/PocketFlow)
- [Discord.py Docs](https://discordpy.readthedocs.io/)

---

## Getting Help

- [GitHub Issues](https://github.com/zhiro-labs/daia/issues) - Report bugs
- [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions) - Ask questions
- [Documentation](https://zhiro-labs.github.io/daia/) - Full guides

---

## Configuration Examples

### Community Support Bot

```bash
ALLOWED_CHANNELS=support-channel-id
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=30
CHAT_TEMPERATURE=0.7
```

System prompt:
```
You are a support assistant. Help users with common questions.
Be patient and friendly. Direct users to documentation when needed.
```

### Personal Assistant

```bash
ALLOWED_CHANNELS=
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=50
CHAT_TEMPERATURE=1.0
```

System prompt:
```
You are a personal AI assistant. Help with research and questions.
Provide detailed, thoughtful responses.
```

### Casual Chat Bot

```bash
ALLOWED_CHANNELS=general-chat-id
ENABLE_CONTEXTUAL_SYSTEM_PROMPT=on
HISTORY_LIMIT=40
CHAT_TEMPERATURE=1.2
```

System prompt:
```
You are a friendly AI hanging out in Discord.
Keep things casual and fun. Use emojis occasionally 😊
```

---

## Performance Tips

- Use `gemini-1.5-flash` for faster responses
- Lower `HISTORY_LIMIT` to reduce token usage
- Reduce `CHAT_TEMPERATURE` for consistency
- Enable caching for repeated queries (future feature)

---

## Security Best Practices

- Never commit `.env` file
- Rotate API keys regularly
- Use environment-specific tokens
- Limit bot permissions to minimum required
- Monitor API usage for anomalies

---

## Troubleshooting Checklist

- [ ] Environment variables set correctly
- [ ] Discord intents enabled
- [ ] Bot has required permissions
- [ ] API keys are valid
- [ ] Python 3.12+ installed
- [ ] Dependencies installed with `uv sync`
- [ ] Fonts downloaded successfully
- [ ] No firewall blocking connections

---

## Version Information

Check versions:

```bash
# Python version
python --version

# uv version
uv --version

# Package versions
uv pip list
```

---

## Next Steps

- Read [Getting Started](getting-started.html) for detailed setup
- Explore [Configuration & Usage](configuration-usage.html) for advanced options
- Check [Development](development.html) to contribute
- Review [Project Structure](project-structure.html) to understand the code
