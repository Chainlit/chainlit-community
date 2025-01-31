# Chainlit Community

[![Discord](https://dcbadge.vercel.app/api/server/ZThrUxbAYw?style=flat)](https://discord.gg/k73SQ3FyUh)
[![CI](https://github.com/Chainlit/chainlit-community/actions/workflows/ci.yaml/badge.svg)](https://github.com/Chainlit/chainlit-community/actions/workflows/ci.yaml)

Community-maintained extensions for [Chainlit](https://chainlit.io/). Provides alternative data layers and storage providers while maintaining full compatibility with Chainlit's core API.

**Quick Links**:

- [Component Architecture](#component-architecture)
- [Contribution Guide](CONTRIBUTING.md)
- [Available Packages](#-current-state)

## 🚀 Project Purpose

Extend Chainlit's capabilities through community-maintained components:

- Alternative data persistence layers
- Cloud storage integrations
- Specialized observability solutions
- Testing utilities

## 🧩 Component Architecture

### Core Components

| Type                | Packages                              | Documentation Links                                                                                                                                        |
| ------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Layers**     | `dynamodb`, `sqlalchemy`, `literalai` | [DynamoDB](packages/data_layers/dynamodb/README.md), [SQL](packages/data_layers/sqlalchemy/README.md), [Literal](packages/data_layers/literalai/README.md) |
| **Storage Clients** | `azure`, `azure_blob`, `gcs`, `s3`    | [Azure](packages/storage_clients/azure/README.md), [GCS](packages/storage_clients/gcs/README.md), [S3](packages/storage_clients/s3/README.md)              |
| **Testing**         | `pytest`                              | [Pytest Plugin](packages/pytest/README.md)                                                                                                                 |

## 🛠️ Getting Started

### For Users

```bash
# Install specific component
pip install chainlit-sqlalchemy[postgres]  # SQLAlchemy data layer
pip install chainlit-s3[s3]                # AWS S3 storage
```

### For Contributors

1. Fork & clone repo
1. Set up development environment:

```bash
uv run pre-commit install --install-hooks
uv sync --all-packages
```

## 🤝 How to Contribute

Key Contribution Areas:

- New storage providers (Cloudflare R2, MinIO, etc)
- Additional database backends
- Enhanced observability integrations
- Performance optimizations
- Documentation improvements

**Process**:

1. Create/claim an issue
1. Develop in dedicated package
1. Add tests & update package README
1. Submit PR with component documentation

[Full contribution guide →](CONTRIBUTING.md)

## 🌍 Current State

**Stable Components** (Full test coverage):

- SQLAlchemy Data Layer (PostgreSQL/SQLite)
- DynamoDB Data Layer
- AWS S3, GCS, Azure Blob & Data Lake Storage Clients
- Pytest Integration
- LiteralAI Observability

### Ongoing

- Maintain compatibility with Chainlit core
- Expand test coverage
- Improve contributor documentation

## 📚 Documentation

Each package maintains its own documentation:

- Implementation guides in package READMEs
- Usage examples in code comments
- Cross-package compatibility notes in [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔗 Core Relationship

This project extends Chainlit through:

- Alternative persistence options
- Specialized storage integrations
- Community-driven experimentation

Chainlit Core focuses on:

- Main application logic
- UI/UX components
- Core LLM integrations

## 📣 Community

- [Discord Discussions](https://discord.gg/k73SQ3FyUh)
- [Twitter Updates](https://twitter.com/chainlit_io)
- [Issue Tracker](https://github.com/chainlit-community/chainlit-community/issues)

## License

*Licensed under [Apache 2.0](LICENSE). Community-driven since 2024.*
