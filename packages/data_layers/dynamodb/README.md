# chainlit-dynamodb

DynamoDB data layer for [Chainlit](https://chainlit.io/).

## DynamoDB Data Layer

This data layer supports Amazon DynamoDB with optional cloud storage integration for elements.

Key features:
- Single table design with efficient query patterns
- Supports storage clients for attachments (S3, Azure Blob)
- User/thread/step/element/feedback storage in DynamoDB
- Built-in pagination and sorting

## Setup Example (DynamoDB + Cloud Storage)

1. Create DynamoDB table using the [CloudFormation template](#table-structure)
2. Install required dependencies:
```bash
# Core requirements
pip install chainlit-dynamodb

# With cloud storage (choose one):
pip install chainlit-dynamodb[s3]          # AWS S3
pip install chainlit-dynamodb[azure-blob] # Azure Blob Storage
pip install chainlit-dynamodb[gcs]        # Google Cloud Storage
pip install chainlit-dynamodb[azure]      # Azure Data Lake
```

3. Configure in your Chainlit app:
```python
import os
import chainlit as cl
from chainlit.data.dynamodb import DynamoDBDataLayer
from chainlit.data.storage_clients import (
    S3StorageClient,
    AzureBlobStorageClient,
    GCSStorageClient,
    AzureStorageClient
)

# Security Note: Always store secrets in environment variables
# Never commit credentials to source control
# Consider using secret managers like AWS Secrets Manager

@cl.data_layer
def get_data_layer():
    # Choose one storage provider:
    
    # AWS S3 Example
    storage_client = S3StorageClient(
        bucket="<your-bucket>",
        region_name="<your-region>",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
    )
    
    # Azure Blob Example
    # storage_client = AzureBlobStorageClient(
    #     container_name="<your-container>",
    #     storage_account="<your-account>",
    #     storage_key="<your-key>"
    # )
    
    # Google Cloud Storage Example
    # storage_client = GCSStorageClient(
    #     project_id="<your-project>",
    #     client_email="<your-email>",
    #     private_key="<your-key>",
    #     bucket_name="<your-bucket>"
    # )
    
    # Azure Data Lake Example
    # storage_client = AzureStorageClient(
    #     account_url="https://<account>.dfs.core.windows.net",
    #     credential="<your-credential>",
    #     container_name="<your-container>"
    # )

    return DynamoDBDataLayer(
        table_name="<your-table-name>",
        storage_provider=storage_client,
        user_thread_limit=10
    )
```

## Table Structure
```yaml
# CloudFormation template for required table structure
AWSTemplateFormatVersion: 2010-09-09
Resources:
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: "<YOUR-TABLE-NAME>"
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
        - AttributeName: UserThreadPK
          AttributeType: S
        - AttributeName: UserThreadSK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: UserThread
          KeySchema:
            - AttributeName: UserThreadPK
              KeyType: HASH
            - AttributeName: UserThreadSK
              KeyType: RANGE
          Projection:
            ProjectionType: INCLUDE
            NonKeyAttributes: [id, name]
      BillingMode: PAY_PER_REQUEST
```

## Logging
```python
import logging
from chainlit import logger

# Enable debug logging for DynamoDB operations
logger.getChild("DynamoDB").setLevel(logging.DEBUG)
```

## Limitations
- Feedback filtering not supported
- Boto3-based implementation uses blocking IO (not async)
- Decimal types in feedback values require special handling

## Design
Uses single-table design with entity prefixes:
- Users: `USER#{identifier}`
- Threads: `THREAD#{thread_id}`
- Steps: `STEP#{step_id}` 
- Elements: `ELEMENT#{element_id}`

Global Secondary Index (UserThread) enables efficient user thread queries.
