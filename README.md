<p align="center">
  <img src="assets/readme/cover.png" alt="Daia: Discord AI Agent" width="800">
</p>

<p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
    <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+">
    <a href="https://github.com/zhiro-labs/daia/actions/workflows/ci.yml"><img src="https://github.com/zhiro-labs/daia/actions/workflows/ci.yml/badge.svg" alt="Build Status"></a>
    <a href="https://github.com/zhiro-labs/daia/actions/workflows/test-matrix.yml"><img src="https://github.com/zhiro-labs/daia/actions/workflows/test-matrix.yml/badge.svg" alt="Cross-Platform Tests"></a>
</p>

Daia (Discord AI Agent) is an intelligent Discord bot built on the [PocketFlow](https://github.com/The-Pocket/PocketFlow) framework. It supports Google Gemini and 20+ LLM providers via [any-llm](https://github.com/mozilla-ai/any-llm) (OpenAI, Anthropic, xAI, Mistral, and more). It provides conversational AI capabilities with advanced features like markdown table rendering, message history processing, and Google Search integration.

## Features

- **Multi-Provider Support**: Works with Google Gemini and 20+ LLM providers via [any-llm](https://github.com/mozilla-ai/any-llm) (OpenAI, Anthropic, xAI, Mistral, etc.).
- **User Recognition**: Recognizes and addresses users by their display name for a personalized experience.
- **Smart Message Processing**: Processes Discord message history with context awareness.
- **Markdown Table Rendering**: Automatically converts markdown tables to images using Noto Sans CJK fonts. Supported languages include but are not limited to English, Simplified Chinese (简体中文), Traditional Chinese (繁體中文), Japanese (日本語), and Korean (한국어).
  <p align="center">
    <img src="assets/readme/table_rendering_showcase.png" alt="Table Rendering Showcase" width="600">
  </p>
- **Smart Chunking**: Automatically splits long messages into smaller chunks, preserving markdown formatting to avoid Discord's character limit.
- **Google Search Integration**: Built-in search capabilities through Gemini tools.
- **Slash Commands**: Includes a `/newchat` command for starting fresh conversation sessions.

## Getting Started

### Prerequisites

- A Discord Bot Token. You can follow the official guide to create one: [Discord Developer Documentation](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).
- An API key for your chosen LLM provider:
  - Google Gemini: [Google AI Studio](https://aistudio.google.com/apikey)
  - OpenAI: [OpenAI Platform](https://platform.openai.com/api-keys)
  - Anthropic: [Anthropic Console](https://console.anthropic.com/)
  - Other providers: See [any-llm supported providers](https://mozilla-ai.github.io/any-llm/providers/)

### Environment

This project requires Python 3.12+. `uv` will gracefully handle the Python version requirement, create a virtual environment, and manage all project dependencies for you.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/zhiro-labs/daia.git
    cd daia
    ```

2.  **Install dependencies:**

    ```bash
    uv sync
    ```

    > ℹ️ **Note:**
    > If you don't have `uv` installed, you can follow the official installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

3.  **Configure your environment and system prompt:**

    - Copy the example files to create your own configuration:
      ```bash
      cp .env.example .env
      cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
      cp config/runtime.yml.example config/runtime.yml
      ```
    - Edit the `.env` file to add your Discord bot token and Gemini API key.
    - Edit `config/chat_sys_prompt.txt` to customize the bot's personality and instructions.
    - Edit `config/runtime.yml` to configure runtime settings and behavior.

4.  **Run the bot:**
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

## Configuration

Daia uses two configuration files:

### Environment Variables (`.env`)

These are set in a `.env` file in the project root:

- `DISCORD_BOT_TOKEN`: Your Discord bot token. **(Required)**
- `CHAT_MODEL_PROVIDER`: The LLM provider to use. Supports `gemini` (default) or `any-llm-{provider}` for other providers via [any-llm](https://github.com/mozilla-ai/any-llm). Examples: `any-llm-openai`, `any-llm-anthropic`, `any-llm-xai`. See [supported providers](https://mozilla-ai.github.io/any-llm/providers/).
- `CHAT_MODEL_API_KEY`: Your API key for the selected provider. **(Required)**
- `CHAT_MODEL`: The model to use (e.g., "gemini-2.5-flash", "gpt-4o-mini", "claude-3-5-sonnet-latest"). **(Required)**
- `CHAT_TEMPERATURE`: Controls the randomness of responses (range: 0.0–2.0). **(Required)**
- `CHAT_SYS_PROMPT_PATH`: The path to the system prompt file. **(Required)**
- `ENABLE_CONTEXTUAL_SYSTEM_PROMPT`: Set to `on` to enable the contextual system prompt, which allows the bot to recognize and address users by their display name. The recommended setting is `on` (as set in `.env.example`). If the variable is not set, it defaults to `off`.

### Runtime Configuration (`config/runtime.yml`)

These settings can be modified at runtime and are stored in `config/runtime.yml`. Most can also be configured via slash commands (requires administrator permissions):

- `allowed_channels`: A list of channel IDs where the bot is allowed to respond without being mentioned. If empty, the bot will only respond to direct messages and mentions. Use `/addchannel`, `/removechannel`, `/listchannels` to manage.
- `allowed_users`: A list of user IDs allowed to DM the bot. Use `/adduser`, `/removeuser`, `/listusers` to manage.
- `timezone`: The timezone for bot operations (e.g., "America/New_York", "Europe/London", "Asia/Tokyo"). Defaults to "UTC". Use `/settimezone` to change.
- `discord_activity`: The activity status displayed for the bot (e.g., "Surfing", "Listening to music"). Use `/setactivity` to change.
- `history_limit`: The maximum number of messages to fetch from the channel history. Defaults to 12. Use `/sethistorylimit` to change.

## Usage

Daia is designed for easy interaction. Here's how you can use its features:

- **Start a Conversation**: To begin interacting with Daia, you have several options:
  - **In allowed channels**: If `ALLOWED_CHANNELS` is configured with specific channel IDs, you can directly send messages in those channels without mentioning the bot.
  - **Mention the bot**: In any channel where the bot has access, mention it (e.g., `@Daia hello!`) to start a conversation.
  - **Direct Message**: Send the bot a Direct Message (DM) to chat privately.

- **Continue the Conversation**: Daia remembers the recent conversation history. You can simply send a new message to continue the conversation without needing to mention the bot again.

- **Start a New Chat Session**: To start a fresh conversation and clear the context, use the `/newchat` slash command. This will make the bot forget the previous conversation history in that channel.

- **Channel Management** (Administrator only): Control which channels the bot can respond to without being mentioned:
  - `/addchannel`: Add the current channel to the bot's allowed list. The bot will respond to all messages in this channel.
  - `/removechannel`: Remove the current channel from the bot's allowed list. The bot will only respond when mentioned.
  - `/listchannels`: View all channels currently in the allowed list.

- **User Management** (Administrator only): Control which users can DM the bot:
  - `/adduser <user>`: Add a user to the bot's allowed DM list. The bot will respond to DMs from this user.
  - `/removeuser <user>`: Remove a user from the bot's allowed DM list. The bot will no longer respond to DMs from this user.
  - `/listusers`: View all users currently in the allowed DM list.

- **Configuration Management** (Administrator only):
  - `/refreshmetadata`: Refresh all channel and user names in the configuration file. Useful when channels or users have been renamed.
  - `/sethistorylimit <limit>`: Set the number of messages to include in conversation history. This controls how much context the bot remembers from previous messages.
  - `/settimezone <timezone>`: Set the bot's timezone for timestamps. Supports IANA timezone names (e.g., "America/New_York", "Europe/London", "Asia/Tokyo"). Features autocomplete to help you find the right timezone.
  - `/setactivity <activity>`: Set the bot's Discord activity status message (e.g., "Surfing", "Listening to music").

- **Automatic Table Rendering**: When Daia's response contains a markdown table, it will automatically be rendered as an image for better readability. This feature works automatically without any specific commands.

- **Google Search**: If you ask a question that requires up-to-date information, Daia will automatically use its Google Search tool to find the answer.

- **Long Message Handling**: Daia automatically splits long messages into multiple smaller ones, preserving the original formatting. This is an automatic feature to work around Discord's character limit.

## Development

### Setting Up Development Environment

The `dev` branch contains the latest development progress. To start developing:

```bash
# Clone the repository and switch to dev branch
git checkout dev

# Install all dependencies including dev tools
uv sync --dev
```

This installs both production dependencies and development tools like `pytest`, `ruff`, and `pre-commit`.

### Makefile Commands

This project includes a Makefile with convenient shortcuts for common development tasks:

```bash
make help          # Show all available commands
make install       # Install dependencies with uv (includes --dev flag)
make test          # Run tests with pytest
make lint          # Check code quality with ruff
make format        # Auto-format code with ruff
make format-check  # Check if code is properly formatted
make clean         # Remove Python cache files
make ci            # Run all CI checks locally (lint + format-check + test)
make all           # Complete workflow (install + lint + format + test)
```

### Development Workflow

1. **Before making changes:**
   ```bash
   make install  # Ensure all dependencies are up to date
   ```

2. **During development:**
   ```bash
   make format   # Auto-format your code
   make lint     # Check for code quality issues
   make test     # Run the test suite
   ```

3. **Before committing:**
   ```bash
   make ci       # Run all checks (same as GitHub Actions)
   ```

The `make ci` command runs the same checks as your GitHub Actions CI, allowing you to catch issues locally before pushing. This saves time by avoiding failed CI runs.

### Troubleshooting CI Failures

If your CI fails or you encounter linting issues:

1. **Check what's wrong locally:**
   ```bash
   make lint          # See specific linting errors
   make format-check  # Check formatting issues
   ```

2. **Fix automatically:**
   ```bash
   make format        # Auto-fix most formatting issues
   ```

3. **Verify the fix:**
   ```bash
   make ci           # Ensure all checks pass before pushing
   ```

### Code Quality Tools

- **Ruff**: Fast Python linter and formatter that handles code style, imports, and common issues
- **Pytest**: Testing framework for running the test suite
- **Pre-commit**: Git hooks that run checks before commits (if configured)

## Project Structure

```
.
├── .env.example
├── .gitignore
├── main.py
├── pyproject.toml
├── README.md
├── Makefile
├── nodes/
│   ├── __init__.py
│   ├── contextual_system_prompt.py
│   ├── fetch_history.py
│   ├── llm_chat.py
│   ├── process_history.py
│   ├── send_response.py
│   ├── table_extractor.py
│   └── table_renderer.py
├── utils/
│   ├── __init__.py
│   ├── config_utils.py
│   ├── discord_helpers.py
│   └── download_font.py
└── ...
```

## Contributing

Contributions are welcome! Please submit pull requests to the `dev` branch. Feel free to open an issue for any bugs or feature requests.

## Todo

### Core Features

- [ ] Reply message rearrange
- [x] Timezone setting
- [ ] daia-ignore tag
- [ ] Image processing
- [ ] YouTube processing
- [ ] Deep search
- [ ] Smart reply channels
- [ ] Gemini safety setting

### Extensibility

- [x] Mozilla [any-llm](https://github.com/mozilla-ai/any-llm) support (OpenAI, Anthropic, xAI, Mistral, and 20+ providers)
- [ ] MCP support
- ~~[ ] OpenAI support~~ (covered by any-llm)
- ~~[ ] OpenAI compatible support~~ (covered by any-llm)
- [ ] Database support
- [ ] Long-term memory
- [ ] Dive deeper cookbook/pocketflow-thinking on [PocketFlow](https://github.com/The-Pocket/PocketFlow)

## Acknowledgments

- Inspired by [PocketFlow](https://github.com/The-Pocket/PocketFlow) by [Zachary Huang](https://github.com/zachary62)
- The cover background photo was shot by [Çağrı KANMAZ](https://www.pexels.com/@cagrikanmaz) on [Pexels](https://www.pexels.com/video/33098418/)
