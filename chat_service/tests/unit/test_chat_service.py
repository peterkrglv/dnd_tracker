from unittest.mock import MagicMock
import asyncio

from chat_service.app.chat_service import ChatService
from chat_service.app.schemas.message_schemas import MessageCreate, Message


def test_post_message_calls_repo():
    svc = ChatService()
    mock_repo = MagicMock()
    expected = Message(uuid="id1", message="hi", campaign="c1")
    mock_repo.create.return_value = expected
    svc.set_repository(mock_repo)

    result = asyncio.run(svc.post_message("c1", MessageCreate(message="hi")))

    mock_repo.create.assert_called_once()
    assert isinstance(result, Message)
    assert result.uuid == expected.uuid


def test_get_messages_calls_repo():
    svc = ChatService()
    mock_repo = MagicMock()
    expected = [Message(uuid="id1", message="hi", campaign="c1")]
    mock_repo.list_by_campaign.return_value = expected
    svc.set_repository(mock_repo)

    result = asyncio.run(svc.get_messages("c1", page=1, per_page=10))

    mock_repo.list_by_campaign.assert_called_once()
    assert isinstance(result, list)
    assert result[0].uuid == "id1"
