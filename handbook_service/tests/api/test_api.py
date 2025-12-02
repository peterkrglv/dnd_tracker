from unittest.mock import AsyncMock, MagicMock

from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.config.dependencies import get_handbook_service as _get_handbook_service_dep
from app.schemas.wiki_schemas import WikiItem
from main import app


def test_get_wiki_list_endpoint_returns_items(client, mocker):
    fake_service = MagicMock()
    fake_service.get_wiki_list = AsyncMock(
        return_value=[
            WikiItem(uuid="id-1", title="Axe", tag="weapon", content="c1"),
        ]
    )

    app.dependency_overrides[_get_handbook_service_dep] = lambda: fake_service

    response = client.get("/api/v1/wiki/")
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data and data[0]["uuid"] == "id-1"
    app.dependency_overrides.pop(_get_handbook_service_dep, None)


def test_get_wiki_item_not_found_returns_404(client, mocker):
    fake_service = MagicMock()
    fake_service.get_wiki_item = AsyncMock(return_value=None)

    app.dependency_overrides[_get_handbook_service_dep] = lambda: fake_service

    response = client.get("/api/v1/wiki/nonexistent-id")
    assert response.status_code == HTTP_404_NOT_FOUND
    app.dependency_overrides.pop(_get_handbook_service_dep, None)
