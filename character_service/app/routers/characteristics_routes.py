from uuid import UUID

from app.services.character_service import CharacterService
from app.services.characteristics_service import CharacteristicsService
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.dependencies import (
    extract_id_from_token,
    get_character_service,
    get_characteristics_service,
)
from app.schemas.characteristics_schemas import (
    CharacteristicsSheetCreate,
    CharacteristicsSheetResponse,
)

stats_router = APIRouter(tags=["Character stats"], prefix="/{character_id}/stats")


@stats_router.get("/", response_model=CharacteristicsSheetResponse)
async def get_character_stats(
    character_id: int,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
    characteristics_service: CharacteristicsService = Depends(
        get_characteristics_service
    ),
):
    character = await character_service.get_character(character_id, user_id)
    if not character or not character.sheet_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stats not found"
        )

    characteristics = await characteristics_service.get_characteristics(
        character.sheet_id
    )
    if not characteristics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Characteristics not found"
        )

    return characteristics


@stats_router.post(
    "/",
    response_model=CharacteristicsSheetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_character_stats(
    character_id: int,
    stats_data: CharacteristicsSheetCreate,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
    characteristics_service: CharacteristicsService = Depends(
        get_characteristics_service
    ),
):
    character = await character_service.get_character(character_id, user_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character not found"
        )

    if character.sheet_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character already has stats",
        )

    characteristics = await characteristics_service.create_characteristics(stats_data)

    success = await character_service.character_repo.set_character_sheet(
        character_id, characteristics.id, user_id
    )
    if not success:
        await characteristics_service.delete_characteristics(characteristics.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to link stats to character",
        )

    return characteristics


@stats_router.put("/", response_model=CharacteristicsSheetResponse)
async def update_character_stats(
    character_id: int,
    stats_data: CharacteristicsSheetCreate,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
    characteristics_service: CharacteristicsService = Depends(
        get_characteristics_service
    ),
):
    character = await character_service.get_character(character_id, user_id)
    if not character or not character.sheet_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stats not found"
        )

    characteristics = await characteristics_service.update_characteristics(
        character.sheet_id, stats_data
    )
    if not characteristics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Characteristics not found"
        )

    return characteristics
