# Chainlit Community

Welcome to the Chainlit Community repository! This project extends and enhances the [Chainlit](https://chainlit.io/) ecosystem through community-driven development and maintenance.

[![Discord](https://dcbadge.vercel.app/api/server/ZThrUxbAYw?style=flat)](https://discord.gg/k73SQ3FyUh)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/chainlit_io.svg?style=social&label=Follow%20%40chainlit_io)](https://twitter.com/chainlit_io)
[![CI](https://github.com/Chainlit/chainlit-community/actions/workflows/ci.yaml/badge.svg)](https://github.com/Chainlit/chainlit-community/actions/workflows/ci.yaml)

## 🌟 About This Project

The Chainlit Community repository is a collaborative space for developers to contribute to the broader Chainlit ecosystem. While the [core Chainlit project](https://github.com/Chainlit/chainlit) focuses on essential features and integrations, this repository serves as a hub for community-maintained extensions, plugins, and integrations.

### Current State

- This repository is separate from the main Chainlit project, allowing for more flexible and community-driven development.
- It hosts a variety of community-contributed extensions and integrations that expand Chainlit's capabilities beyond its core functionality.
- The project is in its early stages, with a growing collection of community contributions.

### Roadmap

1. Establish a clear contribution process and guidelines.
1. Develop and maintain a curated list of community extensions and integrations.
1. Implement a review and testing system for contributed code.
1. Create centralized documentation for all sub-projects in the `docs` folder.
1. Regularly synchronize with the core Chainlit project to ensure compatibility.
1. Foster a vibrant community of contributors and users.

### Project Goals

- Provide a platform for the Chainlit community to extend and enhance the core Chainlit functionality.
- Maintain a high-quality collection of community-driven extensions and integrations.
- Encourage innovation and experimentation within the Chainlit ecosystem.
- Reduce the maintenance burden on the core Chainlit team by distributing responsibility across the community.
- Create a sustainable model for long-term growth and maintenance of the Chainlit ecosystem.
- Foster community collaboration and quality control through shared code reviews, API alignment, and best practices.

### Non-Goals

- Replacing or competing with the core Chainlit project
- Implementing core Chainlit features or functionalities
- Providing official support for Chainlit's core features
- Developing commercial products or services

## 🤝 How to Contribute

We welcome contributions from developers of all skill levels. To get started:

1. Fork this repository and create a new branch for your feature or fix.
1. Develop your contribution, ensuring it follows our coding standards and guidelines.
1. Write tests and documentation for your code.
1. Submit a pull request with a clear description of your changes and their purpose.

For detailed contribution guidelines, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Quality Control and Testing

To maintain high-quality code and reduce technical debt, we enforce the following practices:

- Extensive use of pytest for automated testing
- Type checking and linting
- Minimum 80% test coverage for new code
- Testing against both the latest Chainlit release and the main branch
- Documentation for all added or changed functionality

## Component Architecture

Chainlit Community components follow a modular architecture with two main component types:

### 1. Data Layers
**Role**: Persistent structured data storage for conversation elements (users, threads, steps)  
**Interactions**:  
- Direct integration with Chainlit's data layer system  
- Optional integration with Storage Providers for file attachments  

| Package | Description | README |
|---------|-------------|--------|
| `dynamodb` | Amazon DynamoDB implementation with cloud storage integration | [docs](packages/data_layers/dynamodb/README.md) |
| `sqlalchemy` | SQL database support (PostgreSQL/SQLite) with storage provider integration | [docs](packages/data_layers/sqlalchemy/README.md) |
| `literalai` | Official Literal AI observability platform integration | [docs](packages/data_layers/literalai/README.md) |

### 2. Storage Providers
**Role**: File storage and management for attachments/media  
**Interactions**:  
- Used by Data Layers through dependency injection  
- Handle upload/delete operations and URL generation  

| Package | Cloud Provider | README |
|---------|----------------|--------|
| `azure` | Azure Data Lake | [docs](packages/storage_clients/azure/README.md) |
| `azure-blob` | Azure Blob Storage | [docs](packages/storage_clients/azure_blob/README.md) |
| `gcs` | Google Cloud Storage | [docs](packages/storage_clients/gcs/README.md) |
| `s3` | AWS S3 | [docs](packages/storage_clients/s3/README.md) |

## Typical Data Flow
```mermaid
graph LR
    A[Chainlit App] --> B{Data Layer}
    B -->|Persists metadata| C[(Database)]
    B -->|Delegates files| D[[Storage Provider]]
    D -->|Stores objects| E[(Cloud Storage)]
```

## 📚 Documentation

All documentation for this repository and its sub-projects is centralized in the `docs` folder. This includes setup instructions, usage guides, and API references for each community-maintained feature or integration.

For general Chainlit documentation, please refer to the [official Chainlit documentation](https://docs.chainlit.io).

## 🔗 Relationship to Core Chainlit

The Chainlit Community repository complements the core Chainlit project by:

- Providing a space for experimental and specialized features.
- Allowing faster iteration and innovation outside the core product cycle.
- Distributing maintenance responsibilities across the community.

The core Chainlit project will continue to focus on:

- Essential features and functionality
- Core LLM framework integrations
- LiteralAI backend integration
- Providing a stable API and hooks for developers to build against

This shared repository structure fosters community collaboration, ensures quality control, and promotes alignment on APIs and best practices.

## 📣 Get in Touch

- Join our [Discord community](https://discord.gg/k73SQ3FyUh) for discussions and support.
- Follow us on [Twitter](https://twitter.com/chainlit_io) for updates.
- Report issues or suggest improvements by creating a [GitHub issue](https://github.com/chainlit-community/chainlit-community/issues).

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

______________________________________________________________________

We're excited to see what the community will build with and for Chainlit. Thank you for being a part of this journey!
