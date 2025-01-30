# chainlit-azure-blob

Azure Blob Storage integration for [Chainlit](https://chainlit.io/) applications.

## Features

- Seamless file management with Azure Blob Storage
- Automatic SAS token generation for secure access
- Integrated with Chainlit's data layer system
- Supports both development and production environments

## Quick Start

1. Install the package:
```bash
pip install chainlit-azure-blob[azure-blob]
```

2. Configure in your Chainlit app:
```python
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit_azure_blob import AzureBlobStorageClient

@cl.data_layer
def get_data_layer():
    # Configure Azure Blob Storage
    storage_client = AzureBlobStorageClient(
        container_name="your-container",
        storage_account="your-account",
        storage_key="your-access-key"
    )

    return SQLAlchemyDataLayer(
        conninfo="postgresql+asyncpg://user:password@host/dbname",
        storage_provider=storage_client
    )
```

## Configuration

### Required Parameters
- `container_name`: Your Azure storage container name
- `storage_account`: Azure storage account name
- `storage_key`: Storage account access key (store in environment variables)

> **Security Warning**  
> Always rotate storage keys regularly and monitor access logs

```python
AzureBlobStorageClient(
    container_name="chat-attachments",
    storage_account="myappstorage",
    storage_key="abc123..."
)
```

## Integration Notes

- Files are automatically managed through Chainlit's storage system
- Presigned URLs use 1-hour valid SAS tokens
- Supports automatic MIME type detection
- Overwrite protection enabled by default

## Dependencies

- Azure Blob Storage SDK: `azure-storage-blob>=12.19.0`
- Chainlit compatibility: Requires `chainlit-sqlalchemy` data layer
