from uuid import UUID

from app.db.repos.character_repository import CharacterRepository
from app.schemas.character_schemas import CharacterCreate, CharacterResponse


class CharacterService:
    def __init__(self):
        self.character_repo = None

    def set_repository(self, character_repo: CharacterRepository):
        self.character_repo = character_repo

    async def create_character(
        self, character_data: CharacterCreate, user_id: UUID
    ) -> CharacterResponse:
        character = await self.character_repo.create_character(character_data, user_id)
        return CharacterResponse.from_orm(character)

    async def get_character(
        self, character_id: int, user_id: UUID
    ) -> CharacterResponse | None:
        character = await self.character_repo.get_character_by_id(character_id, user_id)
        if not character:
            return None
        return CharacterResponse.from_orm(character)

    async def update_character(
        self, character_id: int, character_data: CharacterCreate, user_id: UUID
    ) -> CharacterResponse | None:
        character = await self.character_repo.update_character(
            character_id, character_data, user_id
        )
        if not character:
            return None
        return CharacterResponse.from_orm(character)

    async def delete_character(self, character_id: int, user_id: UUID) -> bool:
        return await self.character_repo.delete_character(character_id, user_id)

    async def get_user_characters(self, user_id: UUID) -> list[CharacterResponse]:
        characters = await self.character_repo.get_user_characters(user_id)
        return [CharacterResponse.from_orm(char) for char in characters]
