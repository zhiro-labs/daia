---
layout: default
title: Home
nav_order: 1
---

# Daia: Discord AI Agent

![Daia Cover](assets/cover.png)

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/zhiro-labs/daia/blob/main/LICENSE)
![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
[![CI](https://github.com/zhiro-labs/daia/actions/workflows/ci.yml/badge.svg)](https://github.com/zhiro-labs/daia/actions/workflows/ci.yml)
[![Tests](https://github.com/zhiro-labs/daia/actions/workflows/test-matrix.yml/badge.svg)](https://github.com/zhiro-labs/daia/actions/workflows/test-matrix.yml)

Daia (Discord AI Agent) is an intelligent Discord bot built on the [PocketFlow](https://github.com/The-Pocket/PocketFlow) framework. It supports Google Gemini and 20+ LLM providers via [any-llm](https://github.com/mozilla-ai/any-llm) (OpenAI, Anthropic, xAI, Mistral, and more). It provides conversational AI capabilities with advanced features like markdown table rendering, message history processing, and Google Search integration.

## Features

- **Multi-Provider Support**: Works with Google Gemini and 20+ LLM providers via [any-llm](https://github.com/mozilla-ai/any-llm) (OpenAI, Anthropic, xAI, Mistral, etc.).
- **User Recognition**: Recognizes and addresses users by their display name for a personalized experience.
- **Smart Message Processing**: Processes Discord message history with context awareness.
- **Markdown Table Rendering**: Automatically converts markdown tables to images using Noto Sans CJK fonts. Supported languages include but are not limited to English, Simplified Chinese (简体中文), Traditional Chinese (繁體中文), Japanese (日本語), and Korean (한국어).

  ![Table Rendering Showcase](assets/table_rendering_showcase.png)

- **Smart Chunking**: Automatically splits long messages into smaller chunks, preserving markdown formatting to avoid Discord's character limit.
- **Google Search Integration**: Built-in search capabilities through Gemini tools.
- **Slash Commands**: Includes a `/newchat` command for starting fresh conversation sessions.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/zhiro-labs/daia.git
cd daia

# Install dependencies
uv sync

# Configure
cp .env.example .env
cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
cp config/runtime.yml.example config/runtime.yml
# Edit .env with your tokens

# Run
uv run main.py
```

See [Getting Started](getting-started) for detailed instructions.
