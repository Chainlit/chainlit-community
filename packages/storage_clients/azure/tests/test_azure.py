import pytest
from chainlit_azure import AzureStorageClient


@pytest.fixture
def storage_client():
    return AzureStorageClient(account_url="fsdfds", container="34343")
