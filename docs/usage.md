---
layout: default
title: Usage
nav_order: 4
---

# Usage

Daia is designed for easy interaction. Here's how you can use its features:

## Starting a Conversation

To begin interacting with Daia, you have several options:

- **In allowed channels**: If `ALLOWED_CHANNELS` is configured with specific channel IDs, you can directly send messages in those channels without mentioning the bot.
- **Mention the bot**: In any channel where the bot has access, mention it (e.g., `@Daia hello!`) to start a conversation.
- **Direct Message**: Send the bot a Direct Message (DM) to chat privately.

## Continuing the Conversation

Daia remembers the recent conversation history. You can simply send a new message to continue the conversation without needing to mention the bot again.

## Slash Commands

### General Commands

- `/newchat`: Start a fresh conversation and clear the context. This will make the bot forget the previous conversation history in that channel.

### Channel Management (Administrator only)

Control which channels the bot can respond to without being mentioned:

- `/addchannel`: Add the current channel to the bot's allowed list. The bot will respond to all messages in this channel.
- `/removechannel`: Remove the current channel from the bot's allowed list. The bot will only respond when mentioned.
- `/listchannels`: View all channels currently in the allowed list.

### User Management (Administrator only)

Control which users can DM the bot:

- `/adduser <user>`: Add a user to the bot's allowed DM list. The bot will respond to DMs from this user.
- `/removeuser <user>`: Remove a user from the bot's allowed DM list. The bot will no longer respond to DMs from this user.
- `/listusers`: View all users currently in the allowed DM list.

### Configuration Management (Administrator only)

- `/refreshmetadata`: Refresh all channel and user names in the configuration file. Useful when channels or users have been renamed.
- `/sethistorylimit <limit>`: Set the number of messages to include in conversation history. This controls how much context the bot remembers from previous messages.

## Automatic Features

- **Table Rendering**: When Daia's response contains a markdown table, it will automatically be rendered as an image for better readability.
- **Google Search**: If you ask a question that requires up-to-date information, Daia will automatically use its Google Search tool to find the answer.
- **Long Message Handling**: Daia automatically splits long messages into multiple smaller ones, preserving the original formatting.
