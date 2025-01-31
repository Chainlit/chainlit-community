# Contributing to Chainlit Community

First off, thank you for considering contributing to the Chainlit Community repository! It's people like you that make
Chainlit such a great tool. This document provides guidelines and steps for contributing. Please take a moment to
review this document in order to make the contribution process easy and effective for everyone involved.

## Table of Contents

- [Getting Started](#getting-started)
  - [Issues](#issues)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community Expectations](#community-expectations)

## Getting Started

### Requirements

- [Python](https://python.org/) 3.10-3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setting up

We use uv for package management.

With uv installed, follow these steps to set up your development environment:

1. Install pre-commit hooks: `uv run pre-commit install --install-hooks`
   This will enable automatic formatting, syntax checking and fixups for your contributions.
1. Install dependencies: `uv sync --all-packages`

## 🛠 Development Workflow

### CI Integration

Our CI system (GitHub Actions) automatically runs:

- Formatting checks (Ruff)
- Linting (Ruff)
- Type checking (Pyright)
- Unit tests (pytest) for the latest Chainlit release as well as current `main`,
  across all supported Python versions
- Dependency validation

Verify locally before pushing:

```bash
./scripts/ci.sh  # Runs full test suite
```

### Code Quality

We enforce strict quality controls:

1. **Formatting**:
   ```bash
   uv run ruff format .  # Auto-format code
   ```
1. **Linting**:
   ```bash
   uv run ruff check .  # Validate code standards
   ```
1. **Type Checking**:
   ```bash
   uv run pyright  # Static type analysis
   ```

### Commit Hooks

Pre-commit hooks automatically:

- Format code with Ruff
- Check linting rules
- Validate package structures

Hooks run on every commit - no need to manually format!

### Adding packages

1. Copy (`cp -r`) the package similar to what you want to create, e.g.:
   `cp -r packages/data_layers/sqlalchemy packages/data_layers/bananadb`
1. Rename references to previous data layer in filenames, `pyproject.toml` and `README.md`.
1. Add the package to `members` in `[tool.uv.workspace]` in the root [`pyproject.toml`](pyproject.toml):
   ```toml
   [tool.uv.workspace]
   members = [
      ...
       "packages/data_layers/bananadb",
       ...
   ]
   ```

### Issues

- Feel free to open issues to report bugs, suggest improvements, or propose new features.
- Before opening an issue, please check if a similar issue already exists.
- When reporting a bug, include as much detail as possible, including steps to reproduce, expected behavior, and
  actual behavior.

### Pull Requests

1. Fork the repository and create your branch from `main`.
1. If you've added code that should be tested, add tests.
1. Ensure your code passes all tests and linting.
1. Update the documentation, if necessary.
1. Issue the pull request!

## Coding Standards

- We use [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting. The commit hooks automatically run
  `ruff check .` and `ruff format .` when you commit, but we recommend setting up Ruff and Pyright in your editor.
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use type hints wherever possible.
- Write descriptive variable and function names.

## Editor Setup

### General Recommendations

- Install Ruff & Pyright extensions
- Enable "format on save"
- Set line length to 120 (matches Ruff config)

### VS Code Specific

1. Install extensions:
   - [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
   - [Pyright](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
1. Add to settings.json:
   ```json
   {
     "[python]": {
       "editor.defaultFormatter": "charliermarsh.ruff",
       "editor.formatOnSave": true
     },
     "ruff.importStrategy": "fromEnvironment",
     "python.analysis.typeCheckingMode": "strict"
   }
   ```

## CI/Testing

All components maintain full test coverage of their public APIs. When contributing:

- Add tests for new functionality in `src/tests/`
- Preserve existing test patterns
- Validate against multiple Chainlit versions:
  ```bash
  uv run pytest --chainlit-version=2.0.4,latest,main
  ```

## Community Expectations

- Be respectful and considerate in all communications.
- Adhere to the [Chainlit Code of Conduct](CODE_OF_CONDUCT.md) in all project-related interactions.
- Provide constructive feedback on pull requests.
- Help review other contributors' work.
- Share knowledge and assist others when possible.
- Focus on the goals of the project and avoid scope creep.

Remember, contributions to this repository should align with its goals and not replicate core Chainlit functionality. If
you're unsure whether your contribution fits, feel free to open an issue for discussion first.

Thank you for contributing to Chainlit Community! Your efforts help make Chainlit better for everyone.
