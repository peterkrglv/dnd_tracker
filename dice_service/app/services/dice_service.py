import logging
import random

logger = logging.getLogger("logger")


class DiceService:
    def __init__(self):
        logger.info("DiceService initialized")

    async def roll_dice(self, dice: int) -> int:
        """Бросок одного дайса"""
        if dice <= 0:
            raise ValueError("Dice value must be positive")

        result = random.randint(1, dice)
        logger.info(f"Rolled d{dice}: {result}")
        return result

    async def roll_dice_with_modifiers(
        self, dice: int, mod: int = 0, roll_count: int = 1
    ) -> int:
        """Бросок дайса с модификаторами"""
        if dice <= 0:
            raise ValueError("Dice value must be positive")
        if roll_count <= 0:
            raise ValueError("Roll count must be positive")

        total = 0
        for i in range(roll_count):
            roll = random.randint(1, dice)
            total += roll
            logger.info(f"Roll {i + 1}/{roll_count}: d{dice} = {roll}")

        result = total + mod
        logger.info(f"Total rolls: {total}, mod: {mod}, final result: {result}")
        return result
