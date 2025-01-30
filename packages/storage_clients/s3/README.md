# chainlit-s3

Amazon S3 storage client for [Chainlit](https://chainlit.io/).

## Amazon S3 Storage Client

This storage client enables integration with Amazon S3 for file operations.

Key features:
- File upload/delete operations
- Presigned URL generation
- Automatic URL construction for public objects
- Support for multiple authentication methods
- Seamless integration with boto3 client configuration

## Setup Example

1. Install required dependencies:
```bash
pip install chainlit-s3[s3]
```

2. Configure in your Chainlit app:
```python
# Security Best Practice:
# Prefer IAM roles over access keys for production workloads

import os
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit_s3 import S3StorageClient

@cl.data_layer
def get_data_layer():
    # Example with explicit credentials
    storage_client = S3StorageClient(
        bucket="your-bucket-name",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name="us-west-2"
    )

    return SQLAlchemyDataLayer(
        conninfo="postgresql+asyncpg://user:password@host/dbname",
        storage_provider=storage_client
    )
```

## Authentication Options

### Access Key/Secret
```python
S3StorageClient(
    bucket="your-bucket",
    aws_access_key_id="<ACCESS_KEY>",
    aws_secret_access_key="<SECRET_KEY>",
    region_name="us-west-2"
)
```

### IAM Role
```python
# When running in AWS environment with configured IAM role
S3StorageClient(bucket="your-bucket")
```

### Session Token
```python
S3StorageClient(
    bucket="your-bucket",
    aws_access_key_id="<ACCESS_KEY>",
    aws_secret_access_key="<SECRET_KEY>",
    aws_session_token="<SESSION_TOKEN>",
    region_name="us-west-2"
)
```

## Dependencies

- Required: `boto3`

## Features

### Presigned URLs
Automatically generates presigned URLs with default 1-hour expiration:
```python
url = await storage_client.get_read_url("path/to/object")
```

### Upload Behavior
- Supports both bytes and string data
- Automatic MIME type detection (default: application/octet-stream)
- Returns public URL format: `https://{bucket}.s3.amazonaws.com/{object_key}`

### Error Handling
- Failed operations return empty dict/False
- Detailed warnings logged for troubleshooting

## Notes

1. Required IAM Permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::your-bucket/*"
        }
    ]
}
```

2. Supported boto3 client parameters can be passed directly to the constructor:
```python
S3StorageClient(
    bucket="your-bucket",
    endpoint_url="http://localhost:4566",  # For LocalStack
    config=Config(connect_timeout=30)
)
```

3. Public URL format assumes standard S3 URL structure. For custom domains, subclass and override `sync_upload_file`.
