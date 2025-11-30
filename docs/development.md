---
layout: default
title: Development
nav_order: 5
---

# Development

## Setting Up Development Environment

The `dev` branch contains the latest development progress. To start developing:

```bash
# Clone the repository and switch to dev branch
git checkout dev

# Install all dependencies including dev tools
uv sync --dev
```

This installs both production dependencies and development tools like `pytest`, `ruff`, and `pre-commit`.

## Makefile Commands

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

## Development Workflow

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

The `make ci` command runs the same checks as your GitHub Actions CI, allowing you to catch issues locally before pushing.

## Troubleshooting CI Failures

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

## Code Quality Tools

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
