# chainlit-gcs

Google Cloud Storage client for [Chainlit](https://chainlit.io/).

## Google Cloud Storage Client

This storage client enables integration with Google Cloud Storage for file operations in Chainlit applications.

Key features:
- File upload/delete operations
- Signed URL generation
- Service account authentication
- Base64-encoded private key support

## Setup Example

1. Install required dependencies:
```bash
pip install chainlit-gcs[google-cloud-storage]
```

2. **Configure environment**:
```bash
# .env file
# Security: Never commit this file to version control
GCS_PROJECT_ID="your-project-id"
GCS_CLIENT_EMAIL="service-account-email@project.iam.gserviceaccount.com"
GCS_PRIVATE_KEY="base64_encoded_private_key" 
GCS_BUCKET_NAME="your-bucket-name"
```

3. **Configure in your Chainlit app**:
```python
import os
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit_gcs import GCSStorageClient

@cl.data_layer
def get_data_layer():
    """
    Security Best Practices:
    1. Store credentials in environment variables
    2. Use base64 encoding for private key
    3. Regularly rotate service account keys
    4. Grant minimum required permissions (Storage Object Admin)
    """
    
    # Decoding not needed - client handles base64 encoded key automatically
    private_key = os.environ["GCS_PRIVATE_KEY"]

    storage_client = GCSStorageClient(
        project_id="your-project-id",
        client_email="service-account-email@project.iam.gserviceaccount.com",
        private_key="base64_encoded_private_key",
        bucket_name="your-bucket-name"
    )

    return SQLAlchemyDataLayer(
        conninfo="postgresql+asyncpg://user:password@host/dbname",
        storage_provider=storage_client
    )
```

## Service Account Setup Guide

1. **Create Service Account**:
   - Go to Google Cloud Console > IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Add "Storage Object Admin" role

2. **Generate JSON Key**:
   - Under Actions ⋮ for the service account, select "Manage Keys"
   - Click "Add Key" > "Create New Key" > JSON
   - The key file will download automatically

3. **Encode Private Key**:
```bash
# Encode the private key from the JSON file
cat keyfile.json | jq -r .private_key | base64 -w 0 >> .env
```

## Authentication Configuration

### Service Account Credentials
Obtain credentials from Google Cloud Console:
1. Create a service account with "Storage Admin" role
2. Generate JSON key file
3. Base64 encode the private key value

Example credential configuration:
```python
GCSStorageClient(
    project_id="your-project-id",
    client_email="service-account-email@project.iam.gserviceaccount.com",
    private_key="base64_encoded_private_key",  # Original private key from JSON key file
    bucket_name="your-bucket-name"
)
```

## Operations

### File Upload
- Supports bytes or string data
- Automatic content type detection (default: application/octet-stream)
- Overwrite protection option

### Signed URLs
- Automatically generates v4 signed URLs with expiration
- URLs valid for 1 hour by default

## Dependencies

- Required: `google-cloud-storage`
- Required: `google-oauth2`

## Notes

> **Critical Security Practices**
> - 🔒 Never commit service account keys to version control
> - 🔄 Rotate keys every 90 days minimum
> - 🛡️ Use Google Secret Manager for production deployments
> - 🔐 Set .env file permissions to 600

1. Private key handling:
   - Must be base64 encoded before passing to constructor
   - Original value from service account JSON key file ("private_key" field)
   - Decoding is handled automatically by the client

2. Bucket permissions:
   - Service account requires "Storage Object Admin" IAM role
   - Ensure bucket exists before operations

3. Overwrite behavior:
   - Defaults to True (existing files will be replaced)
   - Set `overwrite=False` to prevent accidental overwrites
