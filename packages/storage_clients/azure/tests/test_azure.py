import pytest
from chainlit_azure import AzureStorageClient


@pytest.fixture
def storage_client(mocker):
    # Mock the required clients
    mock_data_lake_client = mocker.MagicMock()
    mock_container_client = mocker.MagicMock()

    # Create a mock AzureStorageClient
    client = AzureStorageClient(
        account_url="https://mockaccount.dfs.core.windows.net",
        container="test-container",
        credential="mock-credential",
    )

    # Mock the clients
    client.data_lake_client = mock_data_lake_client
    client.container_client = mock_container_client

    # Mock the file client for upload
    mock_file_client = mocker.MagicMock()
    mock_container_client.get_file_client.return_value = mock_file_client

    return client


@pytest.mark.asyncio
async def test_delete_file(storage_client, mocker):
    # Mock the file client for delete
    mock_file_client = mocker.MagicMock()
    storage_client.container_client.get_file_client.return_value = mock_file_client

    # Test delete
    result = await storage_client.delete_file("test_delete.txt")
    assert result is True

    # Verify the delete was called
    mock_file_client.delete_file.assert_called_once()
