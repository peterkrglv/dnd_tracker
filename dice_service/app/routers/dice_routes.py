from starlette.responses import JSONResponse

from dice_service.app.config.dependencies import get_dice_service
from dice_service.app.services.dice_service import DiceService
from dice_service.app.schemas.dice_schemas import (
    DiceRollModRequest,
    DiceRollModResponse,
    DiceRollResponse,
)
from fastapi import APIRouter, Depends

router = APIRouter(tags=["dice"])


@router.get("/dice_roll/{dice}")
async def dice_roll(dice: int, dice_service: DiceService = Depends(get_dice_service)):
    try:
        result = await dice_service.roll_dice(dice)
        return DiceRollResponse(roll_result=result)
    except ValueError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": str(e)}
        )


@router.get("/dice_roll_mod/{dice}")
async def dice_roll_mod(
    dice: int,
    request: DiceRollModRequest,
    dice_service: DiceService = Depends(get_dice_service),
):
    result = await dice_service.roll_dice_with_modifiers(
        dice=dice, mod=request.mod, roll_count=request.roll_count
    )
    return DiceRollModResponse(roll_result=result)
