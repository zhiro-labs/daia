---
layout: default
title: Development
nav_order: 4
---

# Development Guide
{: .no_toc }

Guide for contributing to Daia and extending its functionality.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Setting Up Development Environment

### Prerequisites

- Python 3.12 or higher
- `uv` package manager
- Git
- A code editor (VS Code, PyCharm, etc.)

### Initial Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/daia.git
   cd daia
   ```

2. **Switch to the dev branch:**

   ```bash
   git checkout dev
   ```

   The `dev` branch contains the latest development progress. All pull requests should target this branch.

3. **Install development dependencies:**

   ```bash
   uv sync --dev
   ```

   This installs both production dependencies and development tools like:
   - `pytest` - Testing framework
   - `ruff` - Fast Python linter and formatter
   - `pre-commit` - Git hooks for code quality

4. **Set up pre-commit hooks (optional but recommended):**

   ```bash
   uv run pre-commit install
   ```

   This will automatically run linting and formatting checks before each commit.

---

## Makefile Commands

The project includes a Makefile with convenient shortcuts for common development tasks:

### Available Commands

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

### Common Workflows

**Before starting work:**
```bash
make install  # Ensure dependencies are up to date
```

**During development:**
```bash
make format   # Auto-format your code
make lint     # Check for issues
make test     # Run tests
```

**Before committing:**
```bash
make ci       # Run all checks (same as GitHub Actions)
```

The `make ci` command runs the same checks as GitHub Actions CI, allowing you to catch issues locally before pushing.

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 2. Make Your Changes

Follow the coding standards outlined below. Write clean, well-documented code.

### 3. Test Your Changes

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_specific.py

# Run with coverage
uv run pytest --cov=. --cov-report=html
```

### 4. Lint and Format

```bash
# Auto-format code
make format

# Check for linting issues
make lint

# Run all CI checks
make ci
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Commit message conventions:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub targeting the `dev` branch.

---

## Coding Standards

### Python Style

We use Ruff for linting and formatting, which enforces:

- PEP 8 style guide
- Maximum line length: 100 characters
- Type hints where appropriate
- Docstrings for public functions and classes

### Code Organization

```python
# Standard library imports
import os
from typing import Optional

# Third-party imports
import discord
from google import generativeai as genai

# Local imports
from utils.config_utils import load_config
from nodes.llm_chat import LLMChatNode
```

### Docstrings

Use Google-style docstrings:

```python
def process_message(message: str, user_id: int) -> dict:
    """Process a Discord message and prepare it for the LLM.

    Args:
        message: The message content to process
        user_id: The Discord user ID

    Returns:
        A dictionary containing the processed message data

    Raises:
        ValueError: If the message is empty
    """
    if not message:
        raise ValueError("Message cannot be empty")

    return {"content": message, "user": user_id}
```

### Type Hints

Use type hints for function parameters and return values:

```python
from typing import Optional, List, Dict

def fetch_history(
    channel_id: int,
    limit: int = 50
) -> List[Dict[str, str]]:
    """Fetch message history from a channel."""
    pass
```

---

## Testing

### Writing Tests

Tests are located in the `tests/` directory. Use pytest for testing:

```python
# tests/test_example.py
import pytest
from nodes.process_history import process_history

def test_process_history_basic():
    """Test basic history processing."""
    messages = [
        {"author": "User1", "content": "Hello"},
        {"author": "Bot", "content": "Hi there!"}
    ]

    result = process_history(messages)

    assert len(result) == 2
    assert result[0]["author"] == "User1"

def test_process_history_empty():
    """Test processing empty history."""
    result = process_history([])
    assert result == []
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_example.py

# Run specific test function
uv run pytest tests/test_example.py::test_process_history_basic

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=. --cov-report=html
```

### Test Coverage

Aim for high test coverage, especially for:
- Core functionality (nodes)
- Utility functions
- Error handling paths

---

## Troubleshooting CI Failures

### Linting Failures

If CI fails due to linting issues:

```bash
# Check what's wrong
make lint

# Auto-fix most issues
make format

# Verify the fix
make lint
```

### Test Failures

If tests fail:

```bash
# Run tests locally
make test

# Run with verbose output to see details
uv run pytest -v

# Run specific failing test
uv run pytest tests/test_file.py::test_function -v
```

### Format Check Failures

If format checks fail:

```bash
# Check formatting
make format-check

# Auto-format
make format

# Verify
make format-check
```

---

## Project Architecture

### PocketFlow Framework

Daia is built on PocketFlow, a workflow framework that organizes functionality into nodes. Each node performs a specific task and can be composed into workflows.

### Node Structure

A typical node looks like this:

```python
from pocketflow import Node

class ExampleNode(Node):
    """Example node that processes data."""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    async def run(self, state: dict) -> dict:
        """Execute the node's logic.

        Args:
            state: Current workflow state

        Returns:
            Updated state dictionary
        """
        # Process data
        result = self.process(state["input"])

        # Update state
        state["output"] = result
        return state

    def process(self, data: str) -> str:
        """Process the input data."""
        return data.upper()
```

### Adding a New Node

1. Create a new file in `nodes/`:

   ```python
   # nodes/my_new_node.py
   from pocketflow import Node

   class MyNewNode(Node):
       """Description of what this node does."""

       async def run(self, state: dict) -> dict:
           # Your logic here
           return state
   ```

2. Register the node in `nodes/__init__.py`:

   ```python
   from .my_new_node import MyNewNode

   __all__ = ["MyNewNode", ...]
   ```

3. Use the node in `main.py`:

   ```python
   from nodes import MyNewNode

   # Add to workflow
   workflow.add_node(MyNewNode(config))
   ```

### Adding Utility Functions

Place utility functions in the `utils/` directory:

```python
# utils/my_utils.py
def my_helper_function(data: str) -> str:
    """Helper function description."""
    return data.strip()
```

---

## Adding New Features

### Example: Adding a New Command

1. **Define the command in main.py:**

   ```python
   @bot.tree.command(name="mycommand", description="My new command")
   async def my_command(interaction: discord.Interaction):
       """Handle the new command."""
       await interaction.response.send_message("Command executed!")
   ```

2. **Add any necessary nodes:**

   ```python
   # nodes/my_command_node.py
   class MyCommandNode(Node):
       async def run(self, state: dict) -> dict:
           # Command logic
           return state
   ```

3. **Write tests:**

   ```python
   # tests/test_my_command.py
   def test_my_command():
       # Test the command logic
       pass
   ```

4. **Update documentation:**

   Add the new command to `docs/configuration-usage.md` under the Slash Commands section.

---

## Code Review Guidelines

When reviewing pull requests, check for:

- **Functionality**: Does the code work as intended?
- **Tests**: Are there adequate tests?
- **Documentation**: Is the code well-documented?
- **Style**: Does it follow coding standards?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security issues?

---

## Release Process

Releases are managed by maintainers:

1. Merge `dev` into `main`
2. Tag the release: `git tag v1.0.0`
3. Push tags: `git push --tags`
4. GitHub Actions will build and publish

---

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/zhiro-labs/daia/discussions)
- **Bugs**: Open an [Issue](https://github.com/zhiro-labs/daia/issues)
- **Chat**: Join our Discord (if available)

---

## Resources

- [PocketFlow Documentation](https://github.com/The-Pocket/PocketFlow)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pytest Documentation](https://docs.pytest.org/)
