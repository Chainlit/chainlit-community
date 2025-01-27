import pytest
from chainlit_dynamodb import DynamoDBDataLayer
from types_boto3_dynamodb import DynamoDBClient


@pytest.fixture
def mock_dynamodb_client():
    pass


@pytest.fixture
async def data_layer(mock_dynamodb_client: DynamoDBClient):
    return DynamoDBDataLayer("test_table", mock_dynamodb_client)
