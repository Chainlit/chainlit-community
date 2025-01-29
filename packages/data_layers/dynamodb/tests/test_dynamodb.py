from contextlib import asynccontextmanager
from unittest.mock import ANY, AsyncMock, MagicMock

import pytest
from chainlit.context import ChainlitContext, context_var
from chainlit.element import Text
from chainlit.session import WebsocketSession
from chainlit.types import (
    Feedback,
    Pagination,
    ThreadFilter,
)
from chainlit.user import PersistedUser, User
from chainlit_dynamodb import DynamoDBDataLayer


@pytest.fixture
def mock_context():
    @asynccontextmanager
    async def _context_manager():
        mock_session = MagicMock(spec=WebsocketSession)
        mock_session.user = User(identifier="test_user")
        mock_session.thread_id = "test_thread"
        mock_session.has_first_interaction = True
        mock_session.thread_queues = MagicMock()

        context = ChainlitContext(session=mock_session)
        context.loop = MagicMock()

        token = context_var.set(context)
        try:
            yield context
        finally:
            context_var.reset(token)

    return _context_manager


@pytest.fixture
def mock_dynamodb_client(monkeypatch: pytest.MonkeyPatch):
    mock = MagicMock()
    # Mock boto3 client methods used by the implementation
    mock.get_item = MagicMock()
    mock.put_item = MagicMock()
    mock.update_item = MagicMock()
    mock.delete_item = MagicMock()
    mock.query = MagicMock()
    mock.batch_write_item = MagicMock()
    return mock


@pytest.fixture
async def data_layer(mock_dynamodb_client):
    return DynamoDBDataLayer(
        table_name="test_table",
        client=mock_dynamodb_client,
        storage_provider=AsyncMock(),  # Changed to AsyncMock
        user_thread_limit=5,
    )


async def test_get_user_exists(data_layer):
    test_user = {
        "PK": {"S": "USER#test_user"},
        "SK": {"S": "USER"},
        "id": {"S": "test_id"},
        "identifier": {"S": "test_user"},
        "metadata": {"M": {"key": {"S": "value"}}},
        "createdAt": {"S": "2023-01-01T00:00:00Z"},
    }

    data_layer.client.get_item.return_value = {"Item": test_user}

    user = await data_layer.get_user("test_user")

    assert user == PersistedUser(
        id="test_id",
        identifier="test_user",
        metadata={"key": "value"},
        createdAt="2023-01-01T00:00:00Z",
    )
    data_layer.client.get_item.assert_called_once_with(
        TableName="test_table", Key={"PK": {"S": "USER#test_user"}, "SK": {"S": "USER"}}
    )


async def test_create_user_new(data_layer):
    test_user = User(identifier="new_user", metadata={"key": "value"})

    created_user = await data_layer.create_user(test_user)

    assert created_user is not None
    assert created_user.identifier == "new_user"
    data_layer.client.put_item.assert_called_once_with(TableName="test_table", Item=ANY)


async def test_delete_feedback(data_layer):
    feedback_id = "THREAD#thread123::STEP#step456"
    await data_layer.delete_feedback(feedback_id)

    data_layer.client.update_item.assert_called_once_with(
        TableName="test_table",
        Key={"PK": {"S": "THREAD#thread123"}, "SK": {"S": "STEP#step456"}},
        UpdateExpression="REMOVE #feedback",
        ExpressionAttributeNames={"#feedback": "feedback"},
    )


async def test_upsert_feedback_new(data_layer):
    feedback = Feedback(
        forId="step123", value=1, comment="Great!", threadId="thread123"
    )
    result = await data_layer.upsert_feedback(feedback)

    assert result == "THREAD#thread123::STEP#step123"
    data_layer.client.update_item.assert_called_once_with(
        TableName="test_table",
        Key={"PK": {"S": "THREAD#thread123"}, "SK": {"S": "STEP#step123"}},
        UpdateExpression="SET #feedback = :feedback",
        ExpressionAttributeNames={"#feedback": "feedback"},
        ExpressionAttributeValues=ANY,
    )


async def test_create_element(data_layer, mock_context):
    element = Text(
        id="elem123", content="test content", thread_id="test_thread", for_id="step123"
    )

    # Configure mock storage provider response
    data_layer.storage_provider.upload_file.return_value = {
        "url": "https://example.com/test.txt",
        "object_key": "test_user/test_element/test.txt",
    }

    async with mock_context():
        await data_layer.create_element(element)

    # Verify async storage provider call
    data_layer.storage_provider.upload_file.assert_awaited_once()

    # Verify DynamoDB put_item
    data_layer.client.put_item.assert_called_once_with(TableName="test_table", Item=ANY)


async def test_get_element(data_layer):
    mock_element = {
        "id": {"S": "elem123"},
        "type": {"S": "text"},
        "name": {"S": "name"},
        "mime": {"S": "text/plain"},
        "forId": {"S": "step123"},
        "threadId": {"S": "thread123"},
    }
    data_layer.client.get_item.return_value = {"Item": mock_element}

    element_dict = await data_layer.get_element("thread123", "elem123")

    # Match all properties from mock_element
    assert element_dict["id"] == "elem123"
    assert element_dict["type"] == "text"
    assert element_dict["name"] == "name"
    assert element_dict["mime"] == "text/plain"
    assert element_dict["forId"] == "step123"
    assert element_dict["threadId"] == "thread123"


async def test_delete_step(data_layer, mock_context):
    async with mock_context():
        await data_layer.delete_step("step123")

    # Verify DynamoDB delete_item with expected key structure
    data_layer.client.delete_item.assert_called_once_with(
        TableName="test_table",
        Key={"PK": {"S": "THREAD#test_thread"}, "SK": {"S": "STEP#step123"}},
    )


async def test_get_thread_author(data_layer):
    mock_thread = {
        "PK": {"S": "THREAD#thread123"},
        "SK": {"S": "THREAD"},
        "userId": {"S": "user123"},
    }
    data_layer.client.get_item.return_value = {"Item": mock_thread}

    author = await data_layer.get_thread_author("thread123")
    assert author == "user123"


async def test_list_threads(data_layer):
    mock_response = {
        "Items": [
            {
                "PK": {"S": "THREAD#thread1"},
                "UserThreadSK": {"S": "TS#2023-01-01"},
                "name": {"S": "Thread 1"},
            }
        ],
        "LastEvaluatedKey": {"key": "value"},
    }
    data_layer.client.query.return_value = mock_response

    result = await data_layer.list_threads(
        pagination=Pagination(first=5),
        filters=ThreadFilter(userId="user123", search="test"),
    )

    assert len(result.data) == 1
    assert result.pageInfo.hasNextPage is True
    data_layer.client.query.assert_called_once_with(
        TableName="test_table",
        IndexName="UserThread",
        ScanIndexForward=False,
        Limit=5,
        KeyConditionExpression="#UserThreadPK = :pk",
        ExpressionAttributeNames={"#UserThreadPK": "UserThreadPK", "#name": "name"},
        ExpressionAttributeValues={
            ":pk": {"S": "USER#user123"},
            ":search": {"S": "test"},
        },
        FilterExpression="contains(#name, :search)",
    )


async def test_get_thread(data_layer):
    mock_items = [
        {
            "PK": {"S": "THREAD#thread123"},
            "SK": {"S": "THREAD"},
            "id": {"S": "thread123"},
            "name": {"S": "Test Thread"},
        },
        {
            "PK": {"S": "THREAD#thread123"},
            "SK": {"S": "STEP#step1"},
            "id": {"S": "step1"},
            "createdAt": {"S": "2023-01-01T00:00:00Z"},
        },
    ]
    data_layer.client.query.return_value = {"Items": mock_items}

    thread = await data_layer.get_thread("thread123")

    assert thread["id"] == "thread123"
    assert len(thread["steps"]) == 1


async def test_update_thread(data_layer):
    await data_layer.update_thread(
        "thread123",
        name="Updated Thread",
        user_id="user123",
        metadata={"key": "value"},
        tags=["tag1"],
    )

    data_layer.client.update_item.assert_called_once_with(
        TableName="test_table",
        Key=ANY,
        UpdateExpression=ANY,
        ExpressionAttributeNames=ANY,
        ExpressionAttributeValues=ANY,
    )


async def test_build_debug_url(data_layer):
    url = await data_layer.build_debug_url()
    assert url == ""
