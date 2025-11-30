import pytest
from unittest.mock import patch
from dice_service.app.services.dice_service import DiceService
from dice_service.app.schemas.dice_schemas import DiceRollResponse, DiceRollModResponse, DiceRollModRequest


class TestDiceService:
    """Юнит-тесты для DiceService"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("dice_value,expected_min,expected_max", [
        (6, 1, 6),
        (20, 1, 20),
        (100, 1, 100)
    ])
    async def test_roll_dice_valid_values(self, dice_service, dice_value, expected_min, expected_max):
        # Act
        result = await dice_service.roll_dice(dice_value)

        # Assert
        assert expected_min <= result <= expected_max

    @pytest.mark.asyncio
    @pytest.mark.parametrize("invalid_dice", [0, -1, -10])
    async def test_roll_dice_invalid_values(self, dice_service, invalid_dice):
        # Act & Assert
        with pytest.raises(ValueError, match="Dice value must be positive"):
            await dice_service.roll_dice(invalid_dice)

    @pytest.mark.asyncio
    async def test_roll_dice_with_modifiers_basic(self, dice_service):
        # Arrange
        dice = 20
        mod = 5
        roll_count = 1

        # Act
        with patch('random.randint', return_value=10):
            result = await dice_service.roll_dice_with_modifiers(dice, mod, roll_count)

        # Assert
        assert result == 15  # 10 + 5

    @pytest.mark.asyncio
    async def test_roll_dice_with_modifiers_multiple_rolls(self, dice_service):
        # Arrange
        dice = 6
        mod = 2
        roll_count = 3

        # Act
        with patch('random.randint', side_effect=[3, 4, 5]):
            result = await dice_service.roll_dice_with_modifiers(dice, mod, roll_count)

        # Assert
        assert result == 14  # (3+4+5) + 2

    @pytest.mark.asyncio
    @pytest.mark.parametrize("invalid_dice", [0, -1])
    async def test_roll_dice_with_modifiers_invalid_dice(self, dice_service, invalid_dice):
        # Act & Assert
        with pytest.raises(ValueError, match="Dice value must be positive"):
            await dice_service.roll_dice_with_modifiers(invalid_dice, 0, 1)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("invalid_roll_count", [0, -1])
    async def test_roll_dice_with_modifiers_invalid_roll_count(self, dice_service, invalid_roll_count):
        # Act & Assert
        with pytest.raises(ValueError, match="Roll count must be positive"):
            await dice_service.roll_dice_with_modifiers(20, 0, invalid_roll_count)

    @pytest.mark.asyncio
    async def test_roll_dice_with_modifiers_zero_modifier(self, dice_service):
        # Arrange
        dice = 20
        mod = 0
        roll_count = 1

        # Act
        with patch('random.randint', return_value=15):
            result = await dice_service.roll_dice_with_modifiers(dice, mod, roll_count)

        # Assert
        assert result == 15

    @pytest.mark.asyncio
    async def test_roll_dice_with_modifiers_negative_modifier(self, dice_service):
        # Arrange
        dice = 20
        mod = -3
        roll_count = 1

        # Act
        with patch('random.randint', return_value=10):
            result = await dice_service.roll_dice_with_modifiers(dice, mod, roll_count)

        # Assert
        assert result == 7  # 10 - 3


class TestDiceSchemas:
    """Юнит-тесты для Pydantic схем"""

    def test_dice_roll_response_schema(self):
        # Act
        response = DiceRollResponse(roll_result=15)

        # Assert
        assert response.roll_result == 15
        assert response.model_dump() == {"roll_result": 15}

    def test_dice_roll_mod_response_schema(self):
        # Act
        response = DiceRollModResponse(roll_result=22)

        # Assert
        assert response.roll_result == 22
        assert response.model_dump() == {"roll_result": 22}

    def test_dice_roll_mod_request_schema_defaults(self):
        # Act
        request = DiceRollModRequest()

        # Assert
        assert request.mod == 0
        assert request.roll_count == 1

    def test_dice_roll_mod_request_schema_custom_values(self):
        # Act
        request = DiceRollModRequest(mod=5, roll_count=3)

        # Assert
        assert request.mod == 5
        assert request.roll_count == 3

    def test_dice_roll_mod_request_schema_validation(self):
        # Act & Assert - проверяем что схема принимает None значения для опциональных полей
        request = DiceRollModRequest(mod=None, roll_count=None)
        assert request.mod == 0
        assert request.roll_count == 1


class TestSecurityValidation:
    """Тесты для валидации безопасности"""

    @pytest.mark.asyncio
    async def test_roll_dice_very_large_dice(self, dice_service):
        # Act
        result = await dice_service.roll_dice(1000000)

        # Assert
        assert 1 <= result <= 1000000

    @pytest.mark.asyncio
    async def test_roll_dice_with_modifiers_large_values(self, dice_service):
        # Arrange
        dice = 1000
        mod = 10000
        roll_count = 100

        # Act
        result = await dice_service.roll_dice_with_modifiers(dice, mod, roll_count)

        # Assert
        assert result >= 10000 + 100  # минимальное значение: 100 * 1 + 10000
        assert result <= 10000 + 100000  # максимальное значение: 100 * 1000 + 10000