import pytest
from chainlit_azure_blob import AzureBlobStorageClient


@pytest.fixture
def storage_client():
    # Create a mock AzureStorageClient
    client = AzureBlobStorageClient()

    return client
