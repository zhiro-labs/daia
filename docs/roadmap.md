---
layout: default
title: Roadmap
nav_order: 6
---

# Roadmap
{: .no_toc }

Future plans and features for Daia.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

This page outlines planned features and improvements for Daia. If you're interested in contributing to any of these features, check out the [Development Guide](development.html) and feel free to open an issue or pull request!

---

## Core Features

### Reply Message Rearrange
**Status**: Planned

Improve how Daia handles Discord reply chains and threaded conversations. This will allow the bot to better understand context when users reply to specific messages.

**Benefits:**
- Better context awareness in conversations
- Improved handling of threaded discussions
- More accurate responses to specific questions

### Timezone Setting
**Status**: Planned

Allow users to configure timezone preferences for time-sensitive responses.

**Benefits:**
- Accurate time references in responses
- Scheduled features (future)
- Better localization support

### daia-ignore Tag
**Status**: Planned

Add a way for users to mark messages that Daia should ignore, even in allowed channels.

**Usage example:**
```
[daia-ignore] This is a private conversation
```

**Benefits:**
- More control over bot interactions
- Privacy in shared channels
- Reduced noise in bot responses

### Image Processing
**Status**: Planned

Enable Daia to analyze and respond to images shared in Discord.

**Planned capabilities:**
- Image description and analysis
- OCR (text extraction from images)
- Visual question answering
- Meme understanding

**Technical approach:**
- Leverage Gemini's multimodal capabilities
- Support common image formats (PNG, JPG, GIF)
- Handle image attachments and URLs

### YouTube Processing
**Status**: Planned

Allow Daia to understand and summarize YouTube videos.

**Planned capabilities:**
- Video summarization
- Transcript extraction
- Answer questions about video content
- Timestamp references

**Usage example:**
```
User: @Daia summarize this video: [YouTube URL]
Daia: This video discusses... [summary]
```

### Deep Search
**Status**: Planned

Enhanced search capabilities beyond basic Google Search.

**Planned features:**
- Multi-source search aggregation
- Academic paper search
- Code repository search
- Fact-checking and source verification

### Smart Reply Channels
**Status**: Planned

Intelligent channel detection that learns which channels need bot responses.

**Features:**
- Automatic detection of support channels
- Learning from user interactions
- Configurable per-server rules
- Activity-based response triggers

### Gemini Safety Settings
**Status**: Planned

Configurable safety settings for Gemini API responses.

**Configuration options:**
- Harassment threshold
- Hate speech threshold
- Sexually explicit content threshold
- Dangerous content threshold

**Usage:**
```bash
# In .env
GEMINI_SAFETY_HARASSMENT=BLOCK_MEDIUM_AND_ABOVE
GEMINI_SAFETY_HATE_SPEECH=BLOCK_ONLY_HIGH
```

---

## Extensibility

### Mozilla any-llm Support
**Status**: Planned

Integration with Mozilla's [any-llm](https://github.com/mozilla-ai/any-llm) for broader LLM support.

**Benefits:**
- Support for multiple LLM providers
- Easier model switching
- Standardized interface

### MCP Support
**Status**: Planned

Model Context Protocol support for enhanced tool use and context management.

**Benefits:**
- Better tool integration
- Improved context handling
- Standardized protocol support

### OpenAI Support
**Status**: Planned

Native support for OpenAI models (GPT-4, GPT-3.5, etc.).

**Configuration:**
```bash
CHAT_MODEL_PROVIDER=openai
CHAT_MODEL=gpt-4
OPENAI_API_KEY=your_key_here
```

**Benefits:**
- More model choices
- Different pricing options
- Alternative capabilities

### OpenAI Compatible Support
**Status**: Planned

Support for OpenAI-compatible APIs (LocalAI, Ollama, etc.).

**Benefits:**
- Self-hosted models
- Privacy-focused deployments
- Cost reduction for high-volume usage

**Supported platforms:**
- LocalAI
- Ollama
- LM Studio
- Text Generation WebUI

### Database Support
**Status**: Planned

Persistent storage for conversation history and user preferences.

**Planned databases:**
- SQLite (simple deployments)
- PostgreSQL (production)
- MongoDB (flexible schema)

**Features:**
- Conversation history persistence
- User preferences storage
- Analytics and insights
- Cross-session context

### Long-term Memory
**Status**: Planned

Enable Daia to remember information across sessions and conversations.

**Capabilities:**
- User preference learning
- Fact retention
- Relationship understanding
- Context accumulation over time

**Technical approach:**
- Vector database for semantic search
- Periodic memory consolidation
- Privacy-respecting storage

### PocketFlow Deep Dive
**Status**: Planned

Comprehensive cookbook and documentation for PocketFlow integration.

**Planned content:**
- Advanced workflow patterns
- Custom node development
- Performance optimization
- Best practices guide
- Real-world examples

---

## Community Requests

Have an idea for a feature? We'd love to hear it!

- **Open an Issue**: [GitHub Issues](https://github.com/zhiro-labs/daia/issues)
- **Start a Discussion**: [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions)
- **Submit a PR**: Check the [Development Guide](development.html)

---

## Contributing

Want to help build these features? Here's how:

1. **Pick a feature** from the roadmap
2. **Open an issue** to discuss your approach
3. **Fork the repository** and create a feature branch
4. **Implement the feature** following our [coding standards](development.html#coding-standards)
5. **Write tests** for your implementation
6. **Submit a pull request** to the `dev` branch

See the [Development Guide](development.html) for detailed instructions.

---

## Priority

Features are prioritized based on:

- **Community demand**: Features requested by users
- **Impact**: How much value the feature provides
- **Complexity**: Development effort required
- **Dependencies**: Prerequisites and technical requirements

Current high-priority items:
1. Image Processing
2. Database Support
3. OpenAI Support
4. Long-term Memory

---

## Timeline

We don't commit to specific timelines, as Daia is developed by volunteers. However, we aim to:

- Release minor updates monthly
- Release major features quarterly
- Maintain backward compatibility
- Keep documentation up to date

---

## Feedback

Your feedback shapes Daia's future! Let us know:

- Which features you're most excited about
- What problems you're trying to solve
- How you're using Daia
- What could be improved

Join the conversation on [GitHub Discussions](https://github.com/zhiro-labs/daia/discussions).
