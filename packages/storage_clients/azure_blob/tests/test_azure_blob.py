from datetime import datetime

import pytest
from azure.storage.blob.aio import BlobServiceClient
from chainlit_azure_blob.storage_client import AzureBlobStorageClient


@pytest.fixture
def storage_client(mocker):
    # Mock the required clients
    mock_service_client = mocker.Mock(spec=BlobServiceClient)
    mock_container_client = mocker.Mock()

    # Create a test AzureBlobStorageClient
    client = AzureBlobStorageClient(
        container_name="test-container",
        storage_account="test-account",
        storage_key="test-key",
    )

    # Mock the service clients
    client.service_client = mock_service_client
    client.container_client = mock_container_client

    return client


@pytest.mark.asyncio
async def test_upload_file_string(storage_client, mocker):
    # Test with string data
    blob_client = mocker.AsyncMock()
    storage_client.container_client.get_blob_client.return_value = blob_client

    # Mock get_blob_properties to return expected content type
    properties_mock = mocker.Mock()
    properties_mock.content_settings.content_type = "text/plain"
    properties_mock.size = 123
    properties_mock.last_modified = datetime.now()
    properties_mock.etag = "test-etag"
    blob_client.get_blob_properties.return_value = properties_mock

    result = await storage_client.upload_file(
        object_key="test.txt", data="test content", mime="text/plain"
    )

    # Verify the upload was called with correct parameters
    blob_client.upload_blob.assert_called_once_with(
        b"test content", overwrite=True, content_settings=mocker.ANY
    )

    # Verify result has expected fields
    assert "path" in result
    assert "size" in result
    assert "last_modified" in result
    assert "etag" in result
    assert "content_type" in result
    assert result["content_type"] == "text/plain"


@pytest.mark.asyncio
async def test_upload_file_bytes(storage_client, mocker):
    # Test with bytes data
    blob_client = mocker.AsyncMock()
    storage_client.container_client.get_blob_client.return_value = blob_client

    bytes_data = b"binary content"
    result = await storage_client.upload_file(
        object_key="binary.dat", data=bytes_data, mime="application/octet-stream"
    )

    # Verify the upload was called with correct parameters
    blob_client.upload_blob.assert_called_once_with(
        bytes_data, overwrite=True, content_settings=mocker.ANY
    )

    # Verify result
    assert "path" in result
    assert "size" in result
    assert "last_modified" in result


@pytest.mark.asyncio
async def test_delete_file_success(storage_client, mocker):
    # Test successful deletion
    blob_client = mocker.AsyncMock()
    blob_client.delete_blob.return_value = None
    storage_client.container_client.get_blob_client.return_value = blob_client

    result = await storage_client.delete_file("test.txt")
    assert result is True

    blob_client.delete_blob.assert_called_once()


@pytest.mark.asyncio
async def test_delete_file_failure(storage_client, mocker):
    # Test deletion failure
    blob_client = mocker.AsyncMock()
    blob_client.delete_blob.side_effect = Exception("Delete failed")
    storage_client.container_client.get_blob_client.return_value = blob_client

    result = await storage_client.delete_file("test.txt")
    assert result is False


@pytest.mark.asyncio
async def test_get_read_url(storage_client, mocker):
    # Mock datetime for consistent testing
    mock_now = datetime(2025, 1, 1, 12, 0)
    datetime_mock = mocker.patch("chainlit_azure_blob.storage_client.datetime")
    datetime_mock.now.return_value = mock_now

    # Mock the SAS token generation to avoid real key validation
    mocker.patch(
        "chainlit_azure_blob.storage_client.generate_blob_sas",
        return_value="sv=2021-06-08&sr=b&sig=mock-sig",
    )

    result = await storage_client.get_read_url("test.txt")

    # Verify URL structure and SAS token
    base_url = "https://test-account.blob.core.windows.net/test-container/test.txt"
    assert result.startswith(base_url)
    assert "?" in result  # SAS token should be appended
    # Verify SAS token permissions
    assert "sv=2021-06-08" in result  # Verify SAS version
    assert "sr=b" in result  # Verify scope to blob


@pytest.mark.asyncio
async def test_get_read_url_no_storage_key(mocker):
    # Test when storage_key is not provided
    client = AzureBlobStorageClient(
        container_name="test-container",
        storage_account="test-account",
        storage_key="",
    )

    with pytest.raises(Exception, match="Not using Azure Storage"):
        await client.get_read_url("test.txt")
