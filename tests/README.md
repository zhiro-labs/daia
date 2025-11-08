# Test Suite

This directory contains the test suite for the DAIA Discord AI Agent project.

## Test Files

- `conftest.py` - Pytest configuration and shared fixtures
- `test_imports.py` - Tests to verify all modules can be imported successfully
- `test_nodes.py` - Tests for all node classes in the async flow pipeline
- `test_utils.py` - Tests for utility functions (config, font management, message handling)

## Running Tests

Run all tests:
```bash
uv run pytest -v
```

Run with coverage:
```bash
uv run pytest --cov=. --cov-report=html
```

Run specific test file:
```bash
uv run pytest tests/test_utils.py -v
```

## CI/CD Integration

These tests are automatically run by GitHub Actions workflows:
- `.github/workflows/ci.yml` - Main CI pipeline (linting, formatting, tests)
- `.github/workflows/test-matrix.yml` - Cross-platform testing (Ubuntu, macOS, Windows)

## Test Coverage

Current test coverage includes:
- Node initialization tests for all async flow nodes
- Utility function tests (config parsing, message data creation, font checking)
- Import verification for all modules
- Type validation tests

## Adding New Tests

When adding new functionality:
1. Add corresponding tests in the appropriate test file
2. Use the fixtures in `conftest.py` for common test data
3. Follow the existing test structure and naming conventions
4. Ensure all tests pass before committing
