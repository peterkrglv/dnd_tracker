# app/routers/character_routes.py
from uuid import UUID

from app.services.character_service import CharacterService
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.dependencies import extract_id_from_token, get_character_service
from app.schemas.character_schemas import CharacterCreate, CharacterResponse

character_router = APIRouter(tags=["Character"])


@character_router.post(
    "/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED
)
async def create_character(
    character_data: CharacterCreate,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
):
    try:
        character = await character_service.create_character(character_data, user_id)
        return character
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create character: {str(e)}",
        )


@character_router.get("/", response_model=list[CharacterResponse])
async def get_user_characters(
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
):
    characters = await character_service.get_user_characters(user_id)
    return characters


@character_router.get("/{id}", response_model=CharacterResponse)
async def get_character(
    id: int,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
):
    character = await character_service.get_character(id, user_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character not found"
        )
    return character


@character_router.put("/{id}", response_model=CharacterResponse)
async def update_character(
    id: int,
    character_data: CharacterCreate,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
):
    character = await character_service.update_character(id, character_data, user_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character not found"
        )
    return character


@character_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    id: int,
    user_id: UUID = Depends(extract_id_from_token),
    character_service: CharacterService = Depends(get_character_service),
):
    success = await character_service.delete_character(id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character not found"
        )
    return None
