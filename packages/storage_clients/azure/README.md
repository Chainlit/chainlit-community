# chainlit-azure

Azure Data Lake Storage Gen2 client for [Chainlit](https://chainlit.io/).

## Azure Data Lake Storage Client

This storage client enables integration with Azure Data Lake Storage Gen2 for file operations.

Key features:
- File upload/delete operations
- Presigned URL generation
- SAS token support
- Multiple authentication methods (account key, connection string, SAS token)

## Setup Example

1. Install required dependencies:
```bash
pip install chainlit-azure[azure-datalake]
```

2. Configure in your Chainlit app:
```python
# Security Recommendation:
# Use Azure Managed Identity in production
# For local development, use azure-identity DefaultAzureCredential

import os
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit_azure import AzureStorageClient

@cl.data_layer
def get_data_layer():
    # Example with connection string credential
    storage_client = AzureStorageClient(
        account_url="https://<your_account>.dfs.core.windows.net",
        container="<your_container>",
        credential=os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    )

    return SQLAlchemyDataLayer(
        conninfo=os.environ["DATABASE_URL"],
        storage_provider=storage_client
    )
```

## Authentication Options

### Connection String
```python
AzureStorageClient(
    account_url="https://account.dfs.core.windows.net",
    container="container",
    credential="DefaultEndpointsProtocol=https;AccountName=...;AccountKey=..."
)
```

### Account Key
```python
from azure.identity import AzureNamedKeyCredential

credential = AzureNamedKeyCredential("<account_name>", "<account_key>")
AzureStorageClient(
    account_url="https://account.dfs.core.windows.net",
    container="container",
    credential=credential
)
```

### SAS Token
```python
AzureStorageClient(
    account_url="https://account.dfs.core.windows.net",
    container="container",
    credential=None,  # Not needed if using SAS
    sas_token="<your_sas_token>"
)
```

## Dependencies

- Required: `azure-storage-file-datalake`
- Optional: `azure-identity` (for token-based authentication)

## Notes

1. SAS tokens can be generated automatically if:
   - Account key is provided
   - No existing SAS token is configured
   - Read permissions are required for presigned URLs

2. Supported credential types:
   - Connection strings
   - Account keys
   - AzureNamedKeyCredential
   - AzureSasCredential
   - TokenCredential (Azure Active Directory)
