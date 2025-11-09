---
layout: default
title: Getting Started
nav_order: 2
---

## Prerequisites
- Discord Bot Token → [Discord Developer Portal](https://discord.com/developers/applications)
- Google Gemini API Key → [Google AI Studio](https://aistudio.google.com/apikey)
- Python 3.12+ (handled by `uv`)

## Installation
```bash
git clone https://github.com/zhiro-labs/daia.git
cd daia
uv sync
```

> If you don’t have `uv`: https://docs.astral.sh/uv/getting-started/installation/

## Configuration
```bash
cp .env.example .env
cp config/chat_sys_prompt.txt.example config/chat_sys_prompt.txt
```
Edit `.env` with your tokens and edit the system prompt for personality.

## Run
```bash
uv run main.py
```
First run downloads Noto CJK fonts (~100 MB) for table rendering.

## Discord Setup
In the Developer Portal enable:
- **Server Members Intent**
- **Message Content Intent**

Invite the bot with these permissions:
- View Channels
- Send Messages
- Attach Files
- Read Message History
