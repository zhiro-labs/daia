# CI/CD Setup with uv

This project uses `uv` for dependency management and includes comprehensive CI/CD workflows.

## Local Development

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Setup
```bash
# Install dependencies
uv sync --dev

# Run all CI checks locally
make ci

# Individual commands
make lint          # Run ruff linting
make format        # Format code with ruff
make format-check  # Check code formatting
make test          # Run tests
```

## GitHub Actions Workflows

### 1. Quick Check (`.github/workflows/quick-check.yml`)
- **Triggers**: Every push and pull request
- **Purpose**: Fast feedback on basic code quality
- **Runs**: Formatting check, linting, and tests
- **Duration**: ~1-2 minutes

### 2. Main CI (`.github/workflows/ci.yml`)
- **Triggers**: Push to main/develop, PRs to main/develop
- **Purpose**: Comprehensive testing and code quality
- **Includes**:
  - Code formatting and linting
  - Full test suite

### 3. Test Matrix (`.github/workflows/test-matrix.yml`)
- **Triggers**: Push to main, PRs to main
- **Purpose**: Cross-platform and cross-version testing
- **Matrix**:
  - OS: Ubuntu, macOS, Windows
  - Python: 3.12, 3.13
- **Separate lint job** for efficiency

## Configuration Files

- **`pyproject.toml`**: Project metadata, dependencies, and tool configuration
- **`Makefile`**: Local development commands
- **`.github/dependabot.yml`**: Automated dependency updates

## Key Features

✅ **Fast CI**: Uses `uv` for lightning-fast dependency installation
✅ **Code Quality**: Automated formatting and linting with ruff
✅ **Testing**: Comprehensive test suite
✅ **Cross-platform**: Tests on Linux, macOS, and Windows
✅ **Dependency Management**: Automated updates via Dependabot
✅ **Developer Experience**: Local `make` commands mirror CI exactly

## Workflow Status

The CI will fail if:
- Code is not properly formatted (`ruff format --check`)
- Linting issues are found (`ruff check`)
- Any tests fail (`pytest`)

## Adding New Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update all dependencies
uv sync --upgrade
```

The CI will automatically test with the new dependencies on the next push.
