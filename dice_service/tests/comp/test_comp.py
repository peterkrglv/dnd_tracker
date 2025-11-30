from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from dice_service.main import app  # Импорт вашего FastAPI приложения

@pytest.fixture
def client():
    return TestClient(app)

import pytest

@pytest.mark.asyncio
async def test_dice_roll_valid_dice(client):
    """Тест броска кубика с корректным числом граней."""
    response = client.get("/api/v1/dice/dice_roll/6")
    assert response.status_code == 200
    data = response.json()
    assert "roll_result" in data
    assert isinstance(data["roll_result"], int)
    assert 1 <= data["roll_result"] <= 6

@pytest.mark.asyncio
async def test_dice_roll_negative_dice(client):
    """Отрицательное число граней — 422 Unprocessable Entity."""
    response = client.get("/api/v1/dice/dice_roll/-6")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_dice_roll_mod_invalid_mod_type(client):
    """Нечисловой mod — 422."""
    params = {"mod": "abc", "roll_count": 1}
    response = client.get("/api/v1/dice/dice_roll_mod/6", params=params)
    assert response.status_code == 422
