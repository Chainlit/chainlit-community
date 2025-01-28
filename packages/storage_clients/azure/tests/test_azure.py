import pytest
from azure.storage.filedatalake import ContentSettings
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
    mock_file_client.url = (
        "https://mockaccount.dfs.core.windows.net/test-container/test.txt"
    )

    return client


@pytest.mark.asyncio
async def test_upload_file(storage_client, mocker):
    # Test with string data
    result = await storage_client.upload_file(
        object_key="test.txt", data="This is a test file", mime="text/plain"
    )

    # Verify the upload was called with correct parameters
    file_client = storage_client.container_client.get_file_client.return_value
    file_client.upload_data.assert_called_once_with(
        "This is a test file", overwrite=True, content_settings=mocker.ANY
    )

    # Verify content settings
    content_settings = file_client.upload_data.call_args[1]["content_settings"]
    assert isinstance(content_settings, ContentSettings)
    assert content_settings.content_type == "text/plain"

    # Verify the result
    assert result["object_key"] == "test.txt"
    assert (
        "https://mockaccount.dfs.core.windows.net/test-container/test.txt"
        in result["url"]
    )


@pytest.mark.asyncio
async def test_upload_file_bytes(mocker, storage_client):
    # Test with bytes data
    bytes_data = b"Binary content"
    result = await storage_client.upload_file(
        object_key="binary.dat", data=bytes_data, mime="application/octet-stream"
    )

    # Verify the upload was called
    file_client = storage_client.container_client.get_file_client.return_value
    file_client.upload_data.assert_called_once_with(
        bytes_data, overwrite=True, content_settings=mocker.ANY
    )

    assert result["object_key"] == "binary.dat"


@pytest.mark.asyncio
async def test_upload_file_error(mocker):
    # Create client with mocked error
    client = AzureStorageClient(
        account_url="https://mockaccount.dfs.core.windows.net",
        container="test-container",
        credential="invalid-credential",
    )

    # Mock container client to raise an exception
    mock_container_client = mocker.MagicMock()
    mock_file_client = mocker.MagicMock()
    mock_file_client.upload_data.side_effect = Exception("Upload failed")
    mock_container_client.get_file_client.return_value = mock_file_client
    client.container_client = mock_container_client

    # Attempt upload which should fail
    result = await client.upload_file(object_key="test.txt", data="This should fail")
    assert result == {}


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


@pytest.mark.asyncio
async def test_get_read_url(storage_client, mocker):
    # Test with SAS token provided
    storage_client.sas_token = "test-sas-token"  # Add SAS token for test
    result = await storage_client.get_read_url("test.txt")
    assert "https://mockaccount.dfs.core.windows.net/test-container/test.txt" in result
    assert "?" in result  # Verify SAS token is appended
    assert "test-sas-token" in result  # Verify correct SAS token is used


@pytest.mark.asyncio
async def test_get_read_url_error(mocker):
    # Create client with invalid credentials to force error
    client = AzureStorageClient(
        account_url="https://mockaccount.dfs.core.windows.net",
        container="test-container",
        credential="invalid-credential",
    )

    # Mock the container client to raise an exception
    mock_container_client = mocker.MagicMock()
    client.container_client = mock_container_client
    mock_container_client.get_file_client.side_effect = Exception(
        "Get file client failed"
    )

    # Attempt get_read_url which should return the object key
    result = await client.get_read_url("test.txt")
    assert result == "test.txt"
