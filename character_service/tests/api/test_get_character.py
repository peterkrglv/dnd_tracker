import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_character_details_mocked_service(client: AsyncClient):
    MOCK_ID = 999
    MOCK_CHARACTER_DATA = {
        "id": MOCK_ID,
        "name": "Mock Hero",
        "level": 5,
        "max_hp": 50,
        "appearance": "Tall",
        "history": "Ancient",
        "race_id": 1,
        "class_id": 1,
        "sheet_id": 1,
        "char_class": {"name": "Fighter"},
        "race": {"name": "Human"},
        "characteristics": {"str_score": 10},
        "weapons": []
    }

    with patch('app.routers.character_routes.get_character_service') as mock_dep:
        mock_service = AsyncMock()
        mock_service.get_character_details.return_value = MOCK_CHARACTER_DATA
        mock_dep.return_value = mock_service

        response = await client.get(f"/characters/{MOCK_ID}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == MOCK_ID
    assert data["name"] == "Mock Hero"

    mock_service.get_character_details.assert_called_once_with(MOCK_ID)