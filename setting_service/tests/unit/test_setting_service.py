from unittest.mock import MagicMock
import asyncio

from app.setting_service import SettingService
from app.schemas.setting_schemas import SettingCreate, NPCCreate


def test_create_setting_calls_repo():
    svc = SettingService()
    mock_repo = MagicMock()
    expected = MagicMock()
    mock_repo.create.return_value = expected
    svc.set_repository(mock_repo)

    result = asyncio.run(svc.create_setting(SettingCreate(campaign_uuid="c1")))

    mock_repo.create.assert_called_once()
    assert result == expected


def test_add_npc_calls_repo():
    svc = SettingService()
    mock_repo = MagicMock()
    mock_repo.add_npc.return_value = {"name": "Bob", "description": "orc"}
    svc.set_repository(mock_repo)

    result = asyncio.run(svc.add_npc("c1", NPCCreate(name="Bob")))

    mock_repo.add_npc.assert_called_once()
    assert result["name"] == "Bob"
