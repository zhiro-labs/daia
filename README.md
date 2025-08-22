<p align="center">
  <img src="assets/readme/cover.jpg" alt="Daia: Discord AI Agent" width="800">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
    <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+">
</p>

Daia (Discord AI Agent) is an intelligent Discord bot powered by Google Gemini and built on the [PocketFlow](https://github.com/The-Pocket/PocketFlow) framework. It provides conversational AI capabilities with advanced features like markdown table rendering, message history processing, and Google Search integration.

## Features

- **AI-Powered Conversations**: Leverages Google Gemini for natural language understanding and generation.
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

- A Discord Bot Token
- A Google Gemini API Key

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
    
    > [!NOTE] 
    > If you don't have `uv` installed, you can follow the official installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

3.  **Configure your environment and system prompt:**

    - Copy the example files to create your own configuration:
      ```bash
      cp .env.example .env
      cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
      ```
    - Edit the `.env` file to add your Discord bot token and Gemini API key.
    - Edit `config/chat_sys_prompt.txt` to customize the bot's personality and instructions.

4.  **Run the bot:**
    ```bash
    uv run main.py
    ```

## Configuration

Daia is configured using environment variables. These can be set in a `.env` file in the project root.

- `DISCORD_BOT_TOKEN`: Your Discord bot token.
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `ALLOWED_CHANNELS`: A comma-separated list of channel IDs where the bot is allowed to respond.
- `HISTORY_LIMIT`: The maximum number of messages to fetch from the channel history.
- `CHAT_MODEL`: The Gemini model to use (e.g., "gemini-1.5-flash").
- `CHAT_TEMPERATURE`: Controls the randomness of Gemini's responses (range: 0.0–2.0, default: 1.0).
- `CHAT_SYS_PROMPT_PATH`: The path to the system prompt file.
- `ENABLE_CONTEXTUAL_SYSTEM_PROMPT`: Set to `on` to enable the contextual system prompt, which allows the bot to recognize and address users by their display name. Defaults to `on`.
- `LLM_PROVIDER`: The LLM provider to use. Currently supports `gemini`.

## Usage

- **Mention the bot:** Mention the bot in a channel or send it a direct message to start a conversation.
- **Start a new chat:** Use the `/newchat` slash command to start a fresh conversation session.
- **Markdown Tables:** The bot will automatically render any markdown tables in its responses as images.
- **Google Search:** The bot can use Google Search to answer questions about recent events or to find information on the web.

## Project Structure

```
.
├── .env.example
├── .gitignore
├── main.py
├── pyproject.toml
├── README.md
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

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Todo

### Core Features

- [ ] Reply message rearrange
- [ ] Timezone setting
- [ ] Image processing
- [ ] YouTube processing
- [ ] Deep search
- [ ] Smart reply channels
- [ ] Gemini safety setting

### Extensibility

- [ ] MCP support
- [ ] OpenAI support
- [ ] OpenAI compatible support
- [ ] Database support
- [ ] Long-term memory
- [ ] Dive deeper cookbook/pocketflow-thinking on [PocketFlow](https://github.com/The-Pocket/PocketFlow)

## Acknowledgments

The background of the cover image was shot by [Çağrı KANMAZ](https://www.pexels.com/video/33098418/).
