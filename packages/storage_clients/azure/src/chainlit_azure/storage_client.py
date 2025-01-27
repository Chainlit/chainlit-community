import datetime
from typing import TYPE_CHECKING, Any, Dict, Union

from azure.storage.blob import BlobSasPermissions, generate_blob_sas
from azure.storage.filedatalake import (
    ContentSettings,
    DataLakeFileClient,
    DataLakeServiceClient,
    FileSystemClient,
)
from chainlit.data.storage_clients.base import EXPIRY_TIME, BaseStorageClient
from chainlit.logger import logger

if TYPE_CHECKING:
    from azure.core.credentials import (
        AzureNamedKeyCredential,
        AzureSasCredential,
        TokenCredential,
    )


class AzureStorageClient(BaseStorageClient):
    """
    Class to enable Azure Data Lake Storage (ADLS) Gen2

    parms:
        account_url: "https://<your_account>.dfs.core.windows.net"
        credential: Access credential (AzureKeyCredential)
        sas_token: Optionally include SAS token to append to urls
    """

    def __init__(
        self,
        account_url: str,
        container: str,
        credential: Union[
            str,
            Dict[str, str],
            "AzureNamedKeyCredential",
            "AzureSasCredential",
            "TokenCredential",
            None,
        ],
        sas_token: str | None = None,
    ):
        try:
            self.account_url = account_url
            self.credential = credential
            self.data_lake_client = DataLakeServiceClient(
                account_url=account_url, credential=credential
            )
            self.container_client: FileSystemClient = (
                self.data_lake_client.get_file_system_client(file_system=container)
            )
            self.sas_token = sas_token
            logger.info("AzureStorageClient initialized")
        except Exception as e:
            logger.warning(f"AzureStorageClient initialization error: {e}")
            raise  # Re-raise the exception so the error is clear

    async def upload_file(
        self,
        object_key: str,
        data: bytes | str,
        mime: str = "application/octet-stream",
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        try:
            file_client: DataLakeFileClient = self.container_client.get_file_client(
                object_key
            )
            content_settings = ContentSettings(content_type=mime)
            file_client.upload_data(
                data, overwrite=overwrite, content_settings=content_settings
            )
            url = (
                f"{file_client.url}{self.sas_token}"
                if self.sas_token
                else file_client.url
            )
            return {"object_key": object_key, "url": url}
        except Exception as e:
            logger.warning(f"AzureStorageClient, upload_file error: {e}")
            return {}

    async def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from Azure Data Lake storage.

        Args:
            object_key: The key of the file to delete

        Returns:
            bool: True if file was deleted successfully, False otherwise
        """
        try:
            file_client = self.container_client.get_file_client(object_key)
            file_client.delete_file()
            return True
        except Exception as e:
            logger.warning(f"AzureStorageClient, delete_file error: {e}")
            return False

    async def get_read_url(self, object_key: str) -> str:
        """
        Get a presigned URL for reading a file from Azure Data Lake storage.

        Args:
            object_key: The key of the file to get the URL for

        Returns:
            str: Presigned URL that can be used to read the file
        """
        try:
            file_client = self.container_client.get_file_client(object_key)
            base_url = file_client.url

            if self.sas_token:
                return f"{base_url}?{self.sas_token}"

            # Only generate SAS token if we don't have one
            account_name = self.account_url.split(".")[0].split("://")[-1]
            account_key = self.credential if isinstance(self.credential, str) else None

            if not account_key:
                raise ValueError("Account key not found for SAS token generation")

            sas_token = generate_blob_sas(
                account_name=account_name,
                account_key=account_key,
                container_name=self.container_client.file_system_name,
                blob_name=object_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.datetime.utcnow()
                + datetime.timedelta(seconds=EXPIRY_TIME),
            )

            return f"{base_url}?{sas_token}"
        except Exception as e:
            logger.warning(f"AzureStorageClient, get_read_url error: {e}")
            return object_key
