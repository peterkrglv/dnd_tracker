from unittest.mock import MagicMock, AsyncMock

from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from chat_service.main import app
from chat_service.app.config.dependencies import get_chat_service as _get_chat_service_dep
from chat_service.app.schemas.message_schemas import Message, MessageCreate


def test_post_message_endpoint(client):
    fake_service = MagicMock()
    fake_service.post_message = AsyncMock(return_value=Message(uuid="m1", message="hi", campaign="c1"))
    app.dependency_overrides[_get_chat_service_dep] = lambda: fake_service

    response = client.post("/api/v1/chat/c1", json={"message": "hi"})
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["uuid"] == "m1"
    app.dependency_overrides.pop(_get_chat_service_dep, None)


def test_delete_message_returns_204(client):
    fake_service = MagicMock()
    fake_service.delete_message = AsyncMock(return_value=None)
    app.dependency_overrides[_get_chat_service_dep] = lambda: fake_service

    response = client.delete("/api/v1/chat/c1/m1")
    assert response.status_code == HTTP_204_NO_CONTENT
    app.dependency_overrides.pop(_get_chat_service_dep, None)
