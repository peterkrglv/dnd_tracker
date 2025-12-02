from unittest.mock import MagicMock, AsyncMock

from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from main import app
from app.config.dependencies import get_setting_service as _get_setting_service
from app.schemas.setting_schemas import Setting, SettingCreate, NPCCreate


def test_post_setting_endpoint(client):
    fake_service = MagicMock()
    fake_service.create_setting = AsyncMock(return_value=Setting(uuid="s1", campaign_uuid="c1"))
    app.dependency_overrides[_get_setting_service] = lambda: fake_service

    response = client.post("/api/v1/setting", json={"campaign_uuid": "c1"})
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["campaign_uuid"] == "c1"
    app.dependency_overrides.pop(_get_setting_service, None)


def test_add_npc_endpoint(client):
    fake_service = MagicMock()
    fake_service.add_npc = AsyncMock(return_value={"name": "Bob", "description": "orc"})
    app.dependency_overrides[_get_setting_service] = lambda: fake_service

    response = client.post("/api/v1/setting/campaign/c1/npc", json={"name": "Bob"})
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Bob"
    app.dependency_overrides.pop(_get_setting_service, None)
