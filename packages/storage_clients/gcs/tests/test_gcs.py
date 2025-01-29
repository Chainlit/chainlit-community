import pytest
from chainlit_gcs.storage_client import GCSStorageClient


@pytest.fixture
def storage_client(mocker):
    # Mock the entire storage client and credentials
    mock_client = mocker.MagicMock()
    mock_bucket = mocker.MagicMock()
    mock_blob = mocker.MagicMock()

    # Patch the storage client and credentials
    mocker.patch("google.cloud.storage.Client", return_value=mock_client)
    mocker.patch(
        "google.oauth2.service_account.Credentials.from_service_account_info",
        return_value=mocker.MagicMock(),
    )

    # Set up bucket and blob relationships
    mock_client.bucket.return_value = mock_bucket  # Correct method
    mock_bucket.blob.return_value = mock_blob

    # Create test client - credentials will be mocked
    client = GCSStorageClient(
        project_id="test-project",
        client_email="test@example.com",
        private_key="ZHVtbXkta2V5",
        bucket_name="test-bucket",
    )

    # Bypass actual credential initialization
    client.client = mock_client

    # Configure default mock behaviors
    mock_blob.exists.return_value = False
    mock_blob.generate_signed_url.return_value = "gs://mock-url"

    return client


@pytest.mark.asyncio
async def test_upload_file_string(storage_client, mocker):
    # Get reference to blob mock
    mock_bucket = storage_client.client.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    await storage_client.upload_file("test.txt", "test content", "text/plain")

    # Verify calls
    storage_client.client.bucket.assert_called_once_with("test-bucket")
    mock_bucket.blob.assert_called_once_with("test.txt")
    mock_blob.upload_from_string.assert_called_once_with(
        b"test content", content_type="text/plain"
    )


@pytest.mark.asyncio
async def test_upload_file_bytes(storage_client, mocker):
    mock_bucket = storage_client.client.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    await storage_client.upload_file(
        "binary.dat", b"binary content", "application/octet-stream"
    )

    storage_client.client.bucket.assert_called_once_with("test-bucket")
    mock_bucket.blob.assert_called_once_with("binary.dat")
    mock_blob.upload_from_string.assert_called_once_with(
        b"binary content", content_type="application/octet-stream"
    )


@pytest.mark.asyncio
async def test_delete_file_success(storage_client, mocker):
    mock_bucket = storage_client.client.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    result = await storage_client.delete_file("test.txt")

    storage_client.client.bucket.assert_called_once_with("test-bucket")
    mock_bucket.blob.assert_called_once_with("test.txt")
    mock_blob.delete.assert_called_once()
    assert result is True


@pytest.mark.asyncio
async def test_delete_file_failure(storage_client, mocker):
    mock_bucket = storage_client.client.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    mock_blob.delete.side_effect = Exception("Delete failed")

    result = await storage_client.delete_file("test.txt")

    assert result is False


@pytest.mark.asyncio
async def test_get_read_url(storage_client, mocker):
    mock_bucket = storage_client.client.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    mock_blob.generate_signed_url.return_value = "gs://test-url"

    url = await storage_client.get_read_url("test.txt")

    storage_client.client.bucket.assert_called_once_with("test-bucket")
    mock_bucket.blob.assert_called_once_with("test.txt")
    assert url == "gs://test-url"
