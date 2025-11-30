import pytest
from unittest.mock import AsyncMock, patch


class TestDiceEndpoints:
    """Интеграционные тесты для эндпоинтов Dice API"""

    def test_dice_roll_endpoint_success(self, test_client):
        # Arrange & Act
        with patch('app.routers.dice_routes.get_dice_service') as mock_dep:
            mock_service = AsyncMock()
            mock_service.roll_dice.return_value = 15
            mock_dep.return_value = mock_service

            response = test_client.get("/api/v1/dice/dice_roll/20")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["roll_result"] == 15
        mock_service.roll_dice.assert_called_once_with(20)

    # def test_dice_roll_endpoint_invalid_dice(self, test_client):
    #     # Arrange & Act
    #     with patch('app.routers.dice_routes.get_dice_service') as mock_dep:
    #         mock_service = AsyncMock()
    #         mock_service.roll_dice.side_effect = ValueError("Dice value must be positive")
    #         mock_dep.return_value = mock_service
    #
    #         response = test_client.get("/api/v1/dice/dice_roll/0")
    #
    #     # Assert
    #     assert response.status_code == 500

    # def test_dice_roll_mod_endpoint_success(self, test_client):
    #     # Arrange & Act
    #     with patch('app.routers.dice_routes.get_dice_service') as mock_dep:
    #         mock_service = AsyncMock()
    #         mock_service.roll_dice_with_modifiers.return_value = 18
    #         mock_dep.return_value = mock_service
    #
    #         response = test_client.get("/api/v1/dice/dice_roll_mod/20?mod=3&roll_count=2")
    #
    #     # Assert
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["roll_result"] == 18
    #     mock_service.roll_dice_with_modifiers.assert_called_once_with(dice=20, mod=3, roll_count=2)

    # def test_dice_roll_mod_endpoint_default_parameters(self, test_client):
    #     # Arrange & Act
    #     with patch('app.routers.dice_routes.get_dice_service') as mock_dep:
    #         mock_service = AsyncMock()
    #         mock_service.roll_dice_with_modifiers.return_value = 12
    #         mock_dep.return_value = mock_service
    #
    #         response = test_client.get("/api/v1/dice/dice_roll_mod/20")
    #
    #     # Assert
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["roll_result"] == 12
    #     mock_service.roll_dice_with_modifiers.assert_called_once_with(dice=20, mod=0, roll_count=1)

    # def test_dice_roll_mod_endpoint_negative_modifier(self, test_client):
    #     # Arrange & Act
    #     with patch('app.routers.dice_routes.get_dice_service') as mock_dep:
    #         mock_service = AsyncMock()
    #         mock_service.roll_dice_with_modifiers.return_value = 7
    #         mock_dep.return_value = mock_service
    #
    #         response = test_client.get("/api/v1/dice/dice_roll_mod/20?mod=-3")
    #
    #     # Assert
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["roll_result"] == 7
    #     mock_service.roll_dice_with_modifiers.assert_called_once_with(dice=20, mod=-3, roll_count=1)

    def test_root_endpoint(self, test_client):
        # Act
        response = test_client.get("/")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": "Dice Service is running"}

    def test_health_check_endpoint(self, test_client):
        # Act
        response = test_client.get("/health")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "dice"


class TestAPIErrorScenarios:
    """Тесты для сценариев ошибок API"""

    def test_nonexistent_endpoint(self, test_client):
        # Act
        response = test_client.get("/api/v1/nonexistent")

        # Assert
        assert response.status_code == 404

    def test_invalid_http_method(self, test_client):
        # Act
        response = test_client.post("/api/v1/dice/dice_roll/20")

        # Assert
        assert response.status_code == 405  # Method Not Allowed