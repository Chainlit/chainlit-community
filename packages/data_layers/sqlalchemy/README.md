# chainlit-sqlalchemy

SQLAlchemy data layer for [Chainlit](https://chainlit.io/).

## SQLAlchemy Data Layer

This data layer supports PostgreSQL and other SQL databases via SQLAlchemy.

Key features:

- Supports storage clients for attachments (currently: Azure, Azure Blobs, GCS, S3)
- User/thread/step/element/feedback storage in SQL
- Async operations

## Setup Example (PostgreSQL + Azure Blob)

1. Load [schema.sql](schema.sql) into your database.
1. Install required dependencies:

```bash
# For PostgreSQL
pip install chainlit-sqlalchemy[postgres]

# For SQLite
pip install chainlit-sqlalchemy[sqlite]

# With cloud storage
pip install chainlit-sqlalchemy[postgres,gcs]    # PostgreSQL + Google Cloud Storage
pip install chainlit-sqlalchemy[sqlite,azure-blob]  # SQLite + Azure Blob
```

2. Configure in your Chainlit app:

```python
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.data.storage_clients import AzureBlobStorageClient

@cl.data_layer
def get_data_layer():
    storage_client = AzureBlobStorageClient(
        container_name="<your_container>",
        storage_account="<your_account>",
        storage_key="<your_key>"
    )

    return SQLAlchemyDataLayer(
        conninfo="postgresql+asyncpg://user:password@host/dbname",
        storage_provider=storage_client
    )
```

> [!NOTE]
> - Add `+asyncpg` to PostgreSQL connection strings for async support
> - See SQLAlchemy docs for other database connection formats

## Dependencies

- Core: `SQLAlchemy`
- Database Drivers (optional):
  - PostgreSQL: `asyncpg`, `psycopg2-binary`
  - SQLite: `aiosqlite`
- Cloud Storage (optional):
  - Azure (Data Lake): `chainlit-azure`
  - Azure Blob: `chainlit-azure-blob`
  - Google Cloud: `chainlit-gcs`
  - AWS S3: `chainlit-s3`
