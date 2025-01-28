import pytest
from chainlit_gcs import GCSStorageClient


@pytest.fixture
def storage_client() -> GCSStorageClient:
    # Create a mock AzureStorageClient
    client = GCSStorageClient()

    return client
