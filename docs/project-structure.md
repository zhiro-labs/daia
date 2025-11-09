---
layout: default
title: Project Structure
nav_order: 5
---

# Project Structure
{: .no_toc }

Understanding Daia's codebase organization and architecture.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Directory Overview

```
daia/
├── .github/              # GitHub Actions workflows and templates
├── assets/               # Static assets (fonts, images)
│   ├── fonts/           # Downloaded Noto CJK fonts
│   └── readme/          # README images
├── config/              # Configuration files
│   ├── chat_sys_prompt.txt         # System prompt for the bot
│   └── chat_sys_prompt.txt.example # Example system prompt
├── docs/                # Documentation (GitHub Pages)
├── nodes/               # PocketFlow nodes (core functionality)
│   ├── contextual_system_prompt.py
│   ├── fetch_history.py
│   ├── llm_chat.py
│   ├── process_history.py
│   ├── send_response.py
│   ├── table_extractor.py
│   └── table_renderer.py
├── services/            # External service integrations
├── tests/               # Test suite
├── utils/               # Utility functions and helpers
│   ├── config_utils.py
│   ├── discord_helpers.py
│   └── download_font.py
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── main.py             # Application entry point
├── Makefile            # Development commands
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # Project README
└── uv.lock             # Locked dependency versions
```

---

## Core Files

### main.py

The application entry point. Handles:
- Discord bot initialization
- Event handlers (on_message, on_ready)
- Slash command registration
- PocketFlow workflow setup

**Key components:**
```python
# Bot initialization
bot = commands.Bot(command_prefix="!", intents=intents)

# Event handlers
@bot.event
async def on_ready():
    # Bot startup logic

@bot.event
async def on_message(message):
    # Message handling logic

# Slash commands
@bot.tree.command(name="newchat")
async def newchat(interaction):
    # Command logic
```

### pyproject.toml

Project configuration and dependencies. Defines:
- Project metadata (name, version, description)
- Python version requirement (3.12+)
- Dependencies (discord.py, google-generativeai, etc.)
- Development dependencies (pytest, ruff)
- Tool configurations (ruff, pytest)

**Key sections:**
```toml
[project]
name = "daia"
version = "0.1.0"
requires-python = ">=3.12"

[project.dependencies]
discord-py = "^2.3.0"
google-generativeai = "^0.3.0"
pocketflow = "^0.1.0"

[tool.ruff]
line-length = 100
```

---

## Nodes Directory

Nodes are the building blocks of Daia's functionality. Each node performs a specific task in the message processing pipeline.

### contextual_system_prompt.py

**Purpose**: Adds user context to the system prompt

**Functionality:**
- Retrieves user's Discord display name
- Injects user information into the system prompt
- Enables personalized responses

**When it runs**: Before sending messages to the LLM

**State modifications:**
- Reads: `system_prompt`, `user_id`
- Writes: `system_prompt` (enhanced with user context)

### fetch_history.py

**Purpose**: Retrieves message history from Discord

**Functionality:**
- Fetches recent messages from the channel
- Respects the `HISTORY_LIMIT` configuration
- Filters out bot messages (optional)

**When it runs**: At the start of message processing

**State modifications:**
- Reads: `channel`, `limit`
- Writes: `history` (list of message objects)

### llm_chat.py

**Purpose**: Interfaces with Google Gemini API

**Functionality:**
- Sends messages to Gemini
- Handles API errors and retries
- Manages conversation context
- Supports Google Search tool integration

**When it runs**: After history processing

**State modifications:**
- Reads: `messages`, `system_prompt`, `model_config`
- Writes: `response` (LLM response text)

### process_history.py

**Purpose**: Formats message history for the LLM

**Functionality:**
- Converts Discord messages to LLM format
- Handles different message types (text, embeds, attachments)
- Maintains conversation structure
- Filters system messages

**When it runs**: After fetching history

**State modifications:**
- Reads: `history` (raw Discord messages)
- Writes: `messages` (formatted for LLM)

### send_response.py

**Purpose**: Sends bot responses back to Discord

**Functionality:**
- Splits long messages into chunks
- Preserves markdown formatting
- Handles Discord's character limit (2000 chars)
- Manages rate limiting

**When it runs**: After receiving LLM response

**State modifications:**
- Reads: `response`, `channel`
- Writes: None (sends to Discord)

### table_extractor.py

**Purpose**: Identifies markdown tables in responses

**Functionality:**
- Parses markdown text
- Detects table syntax
- Extracts table data
- Validates table structure

**When it runs**: After receiving LLM response

**State modifications:**
- Reads: `response`
- Writes: `tables` (list of table objects)

### table_renderer.py

**Purpose**: Converts markdown tables to images

**Functionality:**
- Renders tables using Pillow (PIL)
- Uses Noto Sans CJK fonts for multilingual support
- Handles table formatting (borders, padding, alignment)
- Generates PNG images

**When it runs**: After table extraction

**State modifications:**
- Reads: `tables`
- Writes: `table_images` (list of image files)

---

## Utils Directory

Utility functions and helper modules used across the project.

### config_utils.py

**Purpose**: Configuration management

**Functions:**
- `load_config()`: Loads environment variables
- `validate_config()`: Validates required settings
- `get_config_value()`: Retrieves specific config values

**Usage:**
```python
from utils.config_utils import load_config

config = load_config()
bot_token = config["DISCORD_BOT_TOKEN"]
```

### discord_helpers.py

**Purpose**: Discord-specific helper functions

**Functions:**
- `chunk_message()`: Splits long messages
- `format_code_block()`: Formats code blocks
- `get_user_display_name()`: Gets user's display name
- `is_bot_mentioned()`: Checks if bot was mentioned

**Usage:**
```python
from utils.discord_helpers import chunk_message

chunks = chunk_message(long_text, max_length=2000)
for chunk in chunks:
    await channel.send(chunk)
```

### download_font.py

**Purpose**: Font management for table rendering

**Functions:**
- `download_fonts()`: Downloads Noto CJK fonts
- `get_font_path()`: Returns path to font files
- `verify_fonts()`: Checks if fonts are available

**Usage:**
```python
from utils.download_font import download_fonts, get_font_path

# On first run
download_fonts()

# When rendering
font_path = get_font_path("NotoSansCJK-Regular.ttc")
```

---

## Configuration Files

### .env

Environment variables for runtime configuration. Not tracked in git.

**Required variables:**
- `DISCORD_BOT_TOKEN`
- `CHAT_MODEL_API_KEY`
- `CHAT_MODEL`
- `CHAT_TEMPERATURE`
- `HISTORY_LIMIT`
- `CHAT_SYS_PROMPT_PATH`

**Optional variables:**
- `DISCORD_BOT_ACTIVITY`
- `ALLOWED_CHANNELS`
- `ENABLE_CONTEXTUAL_SYSTEM_PROMPT`
- `CHAT_MODEL_PROVIDER`

### .env.example

Template for `.env` file. Tracked in git. Contains example values and documentation.

### config/chat_sys_prompt.txt

The system prompt that defines the bot's personality and behavior. This is sent to the LLM with every request.

**Example:**
```
You are Daia, a helpful AI assistant in a Discord server.
You provide clear, accurate information and maintain a friendly tone.
```

---

## Tests Directory

Test suite for the project. Uses pytest framework.

**Structure:**
```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures and configuration
├── test_nodes/          # Tests for nodes
│   ├── test_fetch_history.py
│   ├── test_llm_chat.py
│   └── ...
├── test_utils/          # Tests for utilities
│   ├── test_config_utils.py
│   └── test_discord_helpers.py
└── test_integration/    # Integration tests
    └── test_workflow.py
```

**Running tests:**
```bash
make test                    # Run all tests
pytest tests/test_nodes/     # Run specific directory
pytest -v                    # Verbose output
pytest --cov=.              # With coverage
```

---

## Workflow Architecture

### Message Processing Pipeline

When a user sends a message, it flows through this pipeline:

```
1. Discord Event (on_message)
   ↓
2. Fetch History Node
   ↓
3. Process History Node
   ↓
4. Contextual System Prompt Node (if enabled)
   ↓
5. LLM Chat Node
   ↓
6. Table Extractor Node
   ↓
7. Table Renderer Node (if tables found)
   ↓
8. Send Response Node
```

### State Object

The state object is passed between nodes and contains:

```python
state = {
    "message": discord.Message,      # Original message
    "channel": discord.TextChannel,  # Channel object
    "user_id": int,                  # User ID
    "history": List[dict],           # Raw message history
    "messages": List[dict],          # Formatted messages
    "system_prompt": str,            # System prompt
    "response": str,                 # LLM response
    "tables": List[dict],            # Extracted tables
    "table_images": List[bytes],     # Rendered table images
}
```

---

## Dependencies

### Production Dependencies

- **discord.py**: Discord API wrapper
- **google-generativeai**: Google Gemini API client
- **pocketflow**: Workflow framework
- **Pillow**: Image processing for table rendering
- **python-dotenv**: Environment variable management

### Development Dependencies

- **pytest**: Testing framework
- **ruff**: Linting and formatting
- **pre-commit**: Git hooks
- **pytest-cov**: Test coverage reporting
- **pytest-asyncio**: Async test support

---

## Adding New Components

### Adding a New Node

1. Create file in `nodes/`:
   ```python
   # nodes/my_node.py
   from pocketflow import Node

   class MyNode(Node):
       async def run(self, state: dict) -> dict:
           # Your logic
           return state
   ```

2. Register in `nodes/__init__.py`:
   ```python
   from .my_node import MyNode
   __all__ = [..., "MyNode"]
   ```

3. Add to workflow in `main.py`:
   ```python
   workflow.add_node(MyNode())
   ```

### Adding a New Utility

1. Create file in `utils/`:
   ```python
   # utils/my_util.py
   def my_function(data: str) -> str:
       """Function description."""
       return data.upper()
   ```

2. Import where needed:
   ```python
   from utils.my_util import my_function
   ```

### Adding a New Test

1. Create test file in `tests/`:
   ```python
   # tests/test_my_feature.py
   import pytest

   def test_my_feature():
       assert True
   ```

2. Run tests:
   ```bash
   make test
   ```

---

## Best Practices

### Code Organization

- Keep nodes focused on a single responsibility
- Put shared logic in utils
- Use type hints for better code clarity
- Document complex logic with comments

### State Management

- Don't mutate state unnecessarily
- Always return the state object from nodes
- Use descriptive keys in the state dictionary
- Clean up temporary data after use

### Error Handling

- Use try-except blocks for external API calls
- Log errors with context
- Provide user-friendly error messages
- Don't expose sensitive information in errors

### Performance

- Cache expensive operations
- Use async/await for I/O operations
- Limit history fetch size
- Optimize image rendering

---

## Further Reading

- [PocketFlow Documentation](https://github.com/The-Pocket/PocketFlow)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Development Guide](development.html)
- [Configuration & Usage](configuration-usage.html)
