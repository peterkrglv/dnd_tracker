import pytest
import sys
import os
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from dice_service.app.services.dice_service import DiceService

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dice_service.main import app


@pytest.fixture
def test_client():
    """Фикстура для тестового клиента FastAPI"""
    return TestClient(app)


@pytest.fixture
def dice_service():
    """Фикстура для сервиса броска кубика"""
    return DiceService()


@pytest.fixture
def mock_dice_service():
    """Фикстура для мок-сервиса броска кубика"""
    service = DiceService()
    service.roll_dice = AsyncMock()
    service.roll_dice_with_modifiers = AsyncMock()
    return service