# Contributing to Chainlit Community

First off, thank you for considering contributing to the Chainlit Community repository! It's people like you that make Chainlit such a great tool. This document provides guidelines and steps for contributing. Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

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

### Issues

- Feel free to open issues to report bugs, suggest improvements, or propose new features.
- Before opening an issue, please check if a similar issue already exists.
- When reporting a bug, include as much detail as possible, including steps to reproduce, expected behavior, and actual behavior.

### Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure your code passes all tests and linting.
4. Update the documentation, if necessary.
5. Issue the pull request!

## Development Setup

We use Poetry for package management. Follow these steps to set up your development environment:

1. Install Poetry if you haven't already:
   ```
   pip install poetry
   ```

2. Clone your fork of the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/chainlit-community.git
   cd chainlit-community
   ```

3. Install the project dependencies:
   ```
   poetry install
   ```

4. Activate the virtual environment:
   ```
   poetry shell
   ```

5. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

Now you're ready to start developing!

## Coding Standards

- We use [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting. Run `ruff check .` and `ruff format .` before committing.
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use type hints wherever possible.
- Write descriptive variable and function names.
- Comment your code where necessary, but strive to make it self-documenting.
- For type checking, we use [Pyright](https://github.com/microsoft/pyright).

We strongly recommend setting up Ruff and Pyright in your text editor or IDE. This will help catch potential issues early in the development process.

## Testing

- Write unit tests for all new code using pytest.
- Aim for at least 80% test coverage for any new code.
- Run the full test suite before submitting a pull request:
  ```
  poetry run pytest
  ```
- Tests should be written to work against both the latest Chainlit release and the main branch.

## Documentation

- Update the documentation for any new features or changes to existing functionality.
- Place all documentation in the `docs` folder.
- Use clear, concise language and provide examples where appropriate.
- If you're adding a new feature, include a usage example.

## Community Expectations

- Be respectful and considerate in all communications.
- Adhere to the [Chainlit Code of Conduct](CODE_OF_CONDUCT.md) in all project-related interactions.
- Provide constructive feedback on pull requests.
- Help review other contributors' work.
- Share knowledge and assist others when possible.
- Focus on the goals of the project and avoid scope creep.

Remember, contributions to this repository should align with its goals and not replicate core Chainlit functionality. If you're unsure whether your contribution fits, feel free to open an issue for discussion first.

Thank you for contributing to Chainlit Community! Your efforts help make Chainlit better for everyone.
