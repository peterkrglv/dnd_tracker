import pytest
from httpx import AsyncClient
from typing import Callable
from unittest.mock import patch, AsyncMock

@pytest.fixture
def test_character_data() -> CharacterCreate:
    return CharacterCreate(
        name="Khelben Arunsun",
        level=1,
        race_id=1,
        class_id=2,
        sheet_id=3,
        current_hp=10,
        max_hp=10,
        appearance="Old Wizard",
        history="Archmage of Waterdeep",
        race_id_secondary=None,
        class_id_secondary=None,
        weapons=[]
    )


# --- ФИКСТУРЫ ---

@pytest.fixture
def client() -> AsyncClient:
    return None


@pytest.fixture
def db_session() -> Callable:
    return None


@pytest.fixture
def mock_character_repo() -> AsyncMock:
    return AsyncMock(spec=CharacterRepository)


@pytest.fixture
def test_character_data() -> CharacterCreate:
    return CharacterCreate(
        name="Khelben Arunsun",
        level=1,
        race_id=1,
        class_id=2,
        sheet_id=3,
        current_hp=10,
        max_hp=10,
        appearance="Old Wizard",
        history="Archmage of Waterdeep",
        weapons=[]
    )


@pytest.fixture
def test_user_uuid() -> UUID:
    return UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")

@pytest.mark.asyncio
async def test_service_create_character_success(
        mock_character_repo: AsyncMock, test_character_data: CharacterCreate, test_user_uuid: UUID
):
    service = CharacterService()
    service.set_repository(mock_character_repo)
    MOCK_DB_CHARACTER = {"id": 42, "name": test_character_data.name}
    mock_character_repo.create_character.return_value = MOCK_DB_CHARACTER

    result = await service.create_character(test_character_data, test_user_uuid) # act

    mock_character_repo.create_character.assert_called_once_with(
        test_character_data, test_user_uuid
    )
    assert result["name"] == "Khelben Arunsun"
    assert result["level"] == 1
    assert result["race_id"] == 42
    assert result["class_id"] == 2
    assert result["sheet_id"] == 3
    assert result["current_hp"] == 10
    assert result["max_hp"] == 10
    assert result["appearance"] == "Old Wizard"
    assert result["history"] == "Archmage of Waterdeep"
    assert result["race_id_secondary"] is None
    assert result["class_id_secondary"] is None




