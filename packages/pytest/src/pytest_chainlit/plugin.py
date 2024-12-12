import datetime
from contextlib import asynccontextmanager
from typing import Callable
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from chainlit.context import ChainlitContext, context_var
from chainlit.data.storage_clients.base import BaseStorageClient
from chainlit.session import WebsocketSession
from chainlit.user import PersistedUser, User


@pytest.fixture
def chainlit_persisted_test_user():
    return PersistedUser(
        id="test_user_id",
        createdAt=datetime.datetime.now().isoformat(),
        identifier="test_user_identifier",
    )


@pytest.fixture
def chainlit_mock_storage_client():
    mock_client = AsyncMock(spec=BaseStorageClient)
    mock_client.upload_file.return_value = {
        "url": "https://example.com/test.txt",
        "object_key": "test_user/test_element/test.txt",
    }
    return mock_client


@pytest.fixture
def chainlit_test_user() -> User:
    return User(identifier="test_user_identifier", metadata={})


@pytest.fixture
def chainlit_mock_session_factory(
    chainlit_persisted_test_user: PersistedUser,
) -> Callable[..., Mock]:
    def create_mock_session(**kwargs) -> Mock:
        mock = Mock(spec=WebsocketSession)
        mock.user = kwargs.get("user", chainlit_persisted_test_user)
        mock.id = kwargs.get("id", "test_session_id")
        mock.user_env = kwargs.get("user_env", {"test_env": "value"})
        mock.chat_settings = kwargs.get("chat_settings", {})
        mock.chat_profile = kwargs.get("chat_profile", None)
        mock.http_referer = kwargs.get("http_referer", None)
        mock.client_type = kwargs.get("client_type", "webapp")
        mock.languages = kwargs.get("languages", ["en"])
        mock.thread_id = kwargs.get("thread_id", "test_thread_id")
        mock.emit = AsyncMock()
        mock.has_first_interaction = kwargs.get("has_first_interaction", True)
        mock.files = kwargs.get("files", {})

        return mock

    return create_mock_session


@pytest.fixture
def chainlit_mock_session(chainlit_mock_session_factory) -> Mock:
    return chainlit_mock_session_factory()


@asynccontextmanager
async def _create_chainlit_context(chainlit_mock_session):
    context = ChainlitContext(chainlit_mock_session)
    token = context_var.set(context)
    try:
        yield context
    finally:
        context_var.reset(token)


@pytest_asyncio.fixture
async def chainlit_mock_context(chainlit_persisted_test_user, chainlit_mock_session):
    chainlit_mock_session.user = chainlit_persisted_test_user
    return _create_chainlit_context(chainlit_mock_session)
