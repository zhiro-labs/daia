---
layout: default
title: Troubleshooting
nav_order: 9
---

# Troubleshooting Guide
{: .no_toc }

Detailed solutions for common issues.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Installation Issues

### uv command not found

**Problem**: When running `uv sync`, you get "command not found".

**Solution**:

Install `uv` using one of these methods:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv

# With Homebrew (macOS)
brew install uv
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Python version too old

**Problem**: Error about Python version requirement.

**Solution**:

Daia requires Python 3.12+. Check your version:

```bash
python --version
```

If it's older than 3.12, install a newer version:

```bash
# macOS with Homebrew
brew install python@3.12

# Ubuntu/Debian
sudo apt update
sudo apt install python3.12

# Windows
# Download from python.org
```

Then ensure `uv` uses the correct Python:

```bash
uv python install 3.12
uv sync
```

### Dependency installation fails

**Problem**: `uv sync` fails with dependency errors.

**Solution**:

1. **Clear cache and retry**:
   ```bash
   uv cache clean
   uv sync --reinstall
   ```

2. **Check internet connection**:
   Ensure you can reach PyPI and GitHub.

3. **Update uv**:
   ```bash
   pip install --upgrade uv
   ```

4. **Check for conflicting packages**:
   ```bash
   uv pip list
   ```

---

## Configuration Issues

### .env file not found

**Problem**: Bot can't find environment variables.

**Solution**:

1. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Verify location**:
   The `.env` file must be in the project root directory (same level as `main.py`).

3. **Check file permissions**:
   ```bash
   ls -la .env
   chmod 644 .env
   ```

### Invalid Discord Bot Token

**Problem**: "Improper token has been passed" error.

**Solution**:

1. **Verify token format**:
   Discord tokens look like: `MTIzNDU2Nzg5.AbCdEf.XyZ123-TokenExample`

2. **Regenerate token**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to "Bot" section
   - Click "Reset Token"
   - Copy the new token to `.env`

3. **Check for extra spaces**:
   ```bash
   # Wrong
   DISCORD_BOT_TOKEN= your_token_here

   # Correct
   DISCORD_BOT_TOKEN=your_token_here
   ```

4. **Verify token is active**:
   Make sure you didn't delete the bot in the Developer Portal.

### Invalid Gemini API Key

**Problem**: "API key not valid" error.

**Solution**:

1. **Verify key in Google AI Studio**:
   - Go to [Google AI Studio](https://aistudio.google.com/apikey)
   - Check that the key is active
   - Copy it exactly (no spaces)

2. **Check API quota**:
   - Ensure you haven't exceeded your quota
   - Check usage in Google AI Studio

3. **Verify key format**:
   Gemini keys look like: `AIzaSyD1234567890abcdefghijklmnopqrstuv`

4. **Create new key if needed**:
   If the key is invalid, create a new one in Google AI Studio.

### System prompt file not found

**Problem**: Can't find `chat_sys_prompt.txt`.

**Solution**:

1. **Create the file**:
   ```bash
   cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
   ```

2. **Verify path in .env**:
   ```bash
   CHAT_SYS_PROMPT_PATH=config/chat_sys_prompt.txt
   ```

3. **Check file exists**:
   ```bash
   ls -la config/chat_sys_prompt.txt
   ```

---

## Discord Bot Issues

### Bot doesn't come online

**Problem**: Bot shows as offline in Discord.

**Solution**:

1. **Check console for errors**:
   Look for error messages when starting the bot.

2. **Verify token**:
   Ensure `DISCORD_BOT_TOKEN` is correct.

3. **Check internet connection**:
   Bot needs internet to connect to Discord.

4. **Verify bot wasn't deleted**:
   Check the Developer Portal to ensure the bot still exists.

5. **Check Discord status**:
   Visit [Discord Status](https://discordstatus.com/) to see if there are outages.

### Bot doesn't respond to messages

**Problem**: Bot is online but doesn't reply.

**Solution**:

1. **Enable Message Content Intent**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to "Bot" section
   - Scroll to "Privileged Gateway Intents"
   - Enable "Message Content Intent"
   - Click "Save Changes"
   - **Restart the bot**

2. **Check bot permissions**:
   - Right-click the channel
   - Go to "Edit Channel" → "Permissions"
   - Find your bot
   - Ensure it has:
     - View Channels
     - Send Messages
     - Read Message History

3. **Verify you're using the bot correctly**:
   - In allowed channels: just type
   - In other channels: mention the bot (`@Daia hello`)
   - Or send a DM

4. **Check console for errors**:
   Look for error messages that might indicate the problem.

### Bot can't send messages

**Problem**: Bot receives messages but can't reply.

**Solution**:

1. **Check "Send Messages" permission**:
   Bot needs this permission in the channel.

2. **Check channel restrictions**:
   Some channels may have restrictions on who can send messages.

3. **Verify bot role**:
   Ensure the bot's role isn't restricted by server settings.

4. **Check rate limiting**:
   If sending many messages quickly, Discord may rate limit the bot.

### Slash commands don't appear

**Problem**: `/newchat` command doesn't show up.

**Solution**:

1. **Wait for sync**:
   Commands can take up to an hour to sync globally.

2. **Check bot was invited with correct scope**:
   - Bot needs `applications.commands` scope
   - Re-invite the bot with the correct URL

3. **Restart Discord**:
   Sometimes Discord client needs a restart to see new commands.

4. **Check console for errors**:
   Look for command registration errors.

---

## API and Performance Issues

### Rate limiting errors

**Problem**: "Rate limited" or "Too many requests" errors.

**Solution**:

1. **Reduce request frequency**:
   - Lower `HISTORY_LIMIT` to send fewer tokens
   - Add delays between messages (requires code modification)

2. **Check API quotas**:
   - Discord: 50 requests per second
   - Gemini: Check your tier in Google AI Studio

3. **Implement backoff**:
   The bot should automatically retry with exponential backoff.

4. **Upgrade API tier**:
   Consider upgrading your Gemini API tier for higher limits.

### Slow response times

**Problem**: Bot takes a long time to respond.

**Solution**:

1. **Use faster model**:
   ```bash
   CHAT_MODEL=gemini-1.5-flash
   ```

2. **Reduce history limit**:
   ```bash
   HISTORY_LIMIT=20  # Instead of 50
   ```

3. **Check network latency**:
   Test your connection to Google's API.

4. **Monitor API performance**:
   Check Google AI Studio for API status.

### Out of memory errors

**Problem**: Bot crashes with memory errors.

**Solution**:

1. **Reduce history limit**:
   ```bash
   HISTORY_LIMIT=30
   ```

2. **Restart bot regularly**:
   Set up a cron job or systemd service to restart periodically.

3. **Check for memory leaks**:
   Monitor memory usage over time.

4. **Upgrade server resources**:
   Consider more RAM if running on limited hardware.

---

## Table Rendering Issues

### Tables not rendering as images

**Problem**: Tables appear as text instead of images.

**Solution**:

1. **Check fonts downloaded**:
   Look for "Downloading fonts..." message on first run.

2. **Verify "Attach Files" permission**:
   Bot needs this permission to send images.

3. **Check console for errors**:
   Look for PIL/Pillow errors.

4. **Manually download fonts**:
   ```bash
   uv run python -c "from utils.download_font import download_fonts; download_fonts()"
   ```

5. **Verify font files exist**:
   ```bash
   ls -la assets/fonts/
   ```

### Font download fails

**Problem**: Fonts don't download on first run.

**Solution**:

1. **Check internet connection**:
   Fonts are downloaded from GitHub releases.

2. **Check firewall**:
   Ensure GitHub isn't blocked.

3. **Manual download**:
   - Download from [Noto CJK Releases](https://github.com/notofonts/noto-cjk/releases)
   - Extract to `assets/fonts/`

4. **Retry download**:
   Delete `assets/fonts/` and restart the bot.

### CJK characters not displaying correctly

**Problem**: Chinese/Japanese/Korean characters look wrong.

**Solution**:

1. **Verify Noto CJK fonts installed**:
   ```bash
   ls assets/fonts/ | grep Noto
   ```

2. **Check font file integrity**:
   Re-download if files are corrupted.

3. **Update Pillow**:
   ```bash
   uv pip install --upgrade Pillow
   ```

---

## Message Processing Issues

### Messages getting cut off

**Problem**: Long responses are truncated.

**Solution**:

This shouldn't happen as Daia auto-chunks messages. If it does:

1. **Check console for errors**:
   Look for chunking errors.

2. **Verify latest version**:
   ```bash
   git pull origin main
   uv sync
   ```

3. **Report the issue**:
   Open an issue on GitHub with the message that got cut off.

### Bot responds to itself

**Problem**: Bot replies to its own messages.

**Solution**:

1. **Check message filtering**:
   The bot should ignore its own messages by default.

2. **Verify bot ID check**:
   In `main.py`, ensure:
   ```python
   if message.author == bot.user:
       return
   ```

3. **Update to latest version**:
   This bug should be fixed in recent versions.

### Context not maintained

**Problem**: Bot doesn't remember previous messages.

**Solution**:

1. **Increase history limit**:
   ```bash
   HISTORY_LIMIT=50
   ```

2. **Check history fetching**:
   Look for errors in console related to history.

3. **Verify channel permissions**:
   Bot needs "Read Message History" permission.

4. **Don't use /newchat**:
   This command clears the context.

---

## Development Issues

### Tests failing

**Problem**: `make test` or `pytest` fails.

**Solution**:

1. **Install dev dependencies**:
   ```bash
   uv sync --dev
   ```

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.12+
   ```

3. **Run specific test**:
   ```bash
   uv run pytest tests/test_file.py -v
   ```

4. **Check for import errors**:
   Ensure all dependencies are installed.

### Linting errors

**Problem**: `make lint` shows errors.

**Solution**:

1. **Auto-fix with format**:
   ```bash
   make format
   ```

2. **Check specific errors**:
   ```bash
   uv run ruff check .
   ```

3. **Ignore specific rules** (if needed):
   Add to `pyproject.toml`:
   ```toml
   [tool.ruff]
   ignore = ["E501"]  # Example: ignore line length
   ```

### Pre-commit hooks failing

**Problem**: Git commit is blocked by pre-commit.

**Solution**:

1. **Run hooks manually**:
   ```bash
   uv run pre-commit run --all-files
   ```

2. **Auto-fix issues**:
   ```bash
   make format
   ```

3. **Skip hooks** (not recommended):
   ```bash
   git commit --no-verify
   ```

---

## Deployment Issues

### Bot stops after closing terminal

**Problem**: Bot stops when you close the terminal.

**Solution**:

Use a process manager:

1. **Using screen**:
   ```bash
   screen -S daia
   uv run main.py
   # Press Ctrl+A, then D to detach
   # Reattach with: screen -r daia
   ```

2. **Using tmux**:
   ```bash
   tmux new -s daia
   uv run main.py
   # Press Ctrl+B, then D to detach
   # Reattach with: tmux attach -t daia
   ```

3. **Using systemd** (Linux):
   Create `/etc/systemd/system/daia.service`:
   ```ini
   [Unit]
   Description=Daia Discord Bot
   After=network.target

   [Service]
   Type=simple
   User=your_user
   WorkingDirectory=/path/to/daia
   ExecStart=/path/to/uv run main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then:
   ```bash
   sudo systemctl enable daia
   sudo systemctl start daia
   ```

### Bot crashes randomly

**Problem**: Bot stops unexpectedly.

**Solution**:

1. **Check logs**:
   Look for error messages before crash.

2. **Add error handling**:
   Ensure all async functions have try-except blocks.

3. **Monitor resources**:
   Check CPU and memory usage.

4. **Set up auto-restart**:
   Use systemd or a process manager with restart policies.

5. **Update dependencies**:
   ```bash
   uv sync --upgrade
   ```

---

## Getting More Help

If your issue isn't covered here:

1. **Check console output**:
   Error messages often indicate the problem.

2. **Search GitHub Issues**:
   [github.com/zhiro-labs/daia/issues](https://github.com/zhiro-labs/daia/issues)

3. **Enable debug logging**:
   Add to your code:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Ask for help**:
   - [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions)
   - [Open an Issue](https://github.com/zhiro-labs/daia/issues/new)

5. **Provide details**:
   When asking for help, include:
   - Error messages
   - Console output
   - Steps to reproduce
   - Your configuration (without sensitive data)
   - Python and uv versions

---

## Preventive Measures

### Regular maintenance

```bash
# Update dependencies
uv sync --upgrade

# Clean cache
make clean

# Run tests
make test

# Check for issues
make ci
```

### Monitoring

Set up monitoring for:
- Bot uptime
- API usage and costs
- Error rates
- Response times
- Memory usage

### Backups

Regularly backup:
- `.env` file (securely)
- `config/chat_sys_prompt.txt`
- Any custom modifications

### Security

- Rotate API keys periodically
- Keep dependencies updated
- Monitor for security advisories
- Use environment-specific tokens
- Never commit `.env` to git

---

## Still stuck?

If you've tried everything and still have issues:

1. **Gather information**:
   - Full error message
   - Console output
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)

2. **Open an issue**:
   [github.com/zhiro-labs/daia/issues/new](https://github.com/zhiro-labs/daia/issues/new)

3. **Be patient**:
   Maintainers are volunteers and will help when they can.

4. **Consider contributing**:
   If you solve your issue, consider submitting a PR to help others!
