import os

import boto3  # type: ignore
import pytest
from chainlit_s3 import S3StorageClient
from moto import mock_aws


# Fixtures for setting up the DynamoDB table
@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def s3_mock(aws_credentials):
    """Moto mock S3 setup."""
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        # Create a mock bucket
        s3.create_bucket(Bucket="my-test-bucket")
        yield s3


@pytest.mark.asyncio
async def test_upload_file(s3_mock):
    # Initialize the S3StorageClient with the mock bucket
    client = S3StorageClient(bucket="my-test-bucket")

    # Call the upload_file method and await the result
    result = await client.upload_file(
        object_key="test.txt", data="This is a test file", mime="text/plain"
    )

    # Assert that the file upload returned the correct URL
    assert result["object_key"] == "test.txt"
    assert result["url"] == "https://my-test-bucket.s3.amazonaws.com/test.txt"

    # Verify that the file exists in the mock S3
    response = s3_mock.get_object(Bucket="my-test-bucket", Key="test.txt")
    assert response["Body"].read().decode() == "This is a test file"


@pytest.mark.asyncio
async def test_delete_file(s3_mock):
    # Initialize the S3StorageClient with the mock bucket
    client = S3StorageClient(bucket="my-test-bucket")

    # Upload a test file first
    await client.upload_file(
        object_key="test_delete.txt", data="File to delete", mime="text/plain"
    )

    # Delete the file
    result = await client.delete_file("test_delete.txt")
    assert result is True

    # Verify the file no longer exists
    with pytest.raises(s3_mock.exceptions.NoSuchKey):
        s3_mock.get_object(Bucket="my-test-bucket", Key="test_delete.txt")


@pytest.mark.asyncio
async def test_get_read_url(s3_mock):
    # Initialize the S3StorageClient with the mock bucket
    client = S3StorageClient(bucket="my-test-bucket")

    # Upload a test file first
    await client.upload_file(
        object_key="test_read.txt", data="File to read", mime="text/plain"
    )

    # Get the presigned URL
    url = await client.get_read_url("test_read.txt")

    # Verify the URL contains expected components
    assert "https://" in url
    assert "my-test-bucket" in url
    assert "test_read.txt" in url
    assert "AWSAccessKeyId" in url
    assert "Signature" in url
    assert "Expires" in url


@pytest.mark.asyncio
async def test_upload_file_error():
    # Initialize client with invalid credentials to force error
    client = S3StorageClient(bucket="invalid-bucket", aws_access_key_id="invalid")

    # Attempt upload which should fail
    result = await client.upload_file(object_key="test.txt", data="This is a test file")
    assert result == {}


@pytest.mark.asyncio
async def test_delete_file_error():
    # Initialize client with invalid credentials to force error
    client = S3StorageClient(bucket="invalid-bucket", aws_access_key_id="invalid")

    # Attempt delete which should fail
    result = await client.delete_file("nonexistent.txt")
    assert result is False


@pytest.mark.asyncio
async def test_get_read_url_error():
    # Initialize client with invalid credentials to force error
    client = S3StorageClient(bucket="invalid-bucket", aws_access_key_id="invalid")

    # Attempt to get URL which should return the key
    result = await client.get_read_url("test.txt")
    assert result == "test.txt"


@pytest.mark.asyncio
async def test_upload_file_bytes(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Test with bytes data
    bytes_data = b"Binary content"
    result = await client.upload_file(
        object_key="binary.dat", data=bytes_data, mime="application/octet-stream"
    )

    # Verify upload succeeded
    assert result["object_key"] == "binary.dat"
    response = s3_mock.get_object(Bucket="my-test-bucket", Key="binary.dat")
    assert response["Body"].read() == bytes_data
    assert response["ContentType"] == "application/octet-stream"


@pytest.mark.asyncio
async def test_upload_file_different_mimes(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Test JSON content type
    await client.upload_file(
        object_key="data.json", data='{"key": "value"}', mime="application/json"
    )

    response = s3_mock.get_object(Bucket="my-test-bucket", Key="data.json")
    assert response["ContentType"] == "application/json"

    # Test HTML content type
    await client.upload_file(
        object_key="page.html", data="<html></html>", mime="text/html"
    )

    response = s3_mock.get_object(Bucket="my-test-bucket", Key="page.html")
    assert response["ContentType"] == "text/html"


def test_sync_methods(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Test sync upload
    result = client.sync_upload_file(
        object_key="sync_test.txt", data="Sync upload test", mime="text/plain"
    )
    assert result["object_key"] == "sync_test.txt"

    # Test sync get_read_url
    url = client.sync_get_read_url("sync_test.txt")
    assert "https://" in url
    assert "sync_test.txt" in url

    # Test sync delete
    assert client.sync_delete_file("sync_test.txt") is True


@pytest.mark.asyncio
async def test_upload_file_overwrite(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Upload initial file
    await client.upload_file(
        object_key="overwrite.txt", data="Original content", mime="text/plain"
    )

    # Upload with same key but different content
    await client.upload_file(
        object_key="overwrite.txt", data="New content", mime="text/plain"
    )

    # Verify content was overwritten
    response = s3_mock.get_object(Bucket="my-test-bucket", Key="overwrite.txt")
    assert response["Body"].read().decode() == "New content"


@pytest.mark.asyncio
async def test_unicode_handling(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Test with Unicode content and filename
    unicode_content = "Hello 世界 🌍"
    unicode_filename = "hello_世界_🌍.txt"

    await client.upload_file(
        object_key=unicode_filename,
        data=unicode_content,
        mime="text/plain; charset=utf-8",
    )

    # Verify content was stored correctly
    response = s3_mock.get_object(Bucket="my-test-bucket", Key=unicode_filename)
    assert response["Body"].read().decode() == unicode_content


@pytest.mark.asyncio
async def test_url_expiry(s3_mock):
    client = S3StorageClient(bucket="my-test-bucket")

    # Upload a test file
    await client.upload_file(
        object_key="expiry_test.txt", data="Test content", mime="text/plain"
    )

    # Get URL and verify expiry parameter
    url = await client.get_read_url("expiry_test.txt")
    assert "Expires=" in url

    # Verify expiry is roughly correct (within 5 seconds)
    import time

    from chainlit.data.storage_clients.base import EXPIRY_TIME

    expires_at = int(url.split("Expires=")[1].split("&")[0])
    expected_expiry = int(time.time()) + EXPIRY_TIME
    assert abs(expires_at - expected_expiry) < 5
