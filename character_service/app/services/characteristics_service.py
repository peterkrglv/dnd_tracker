# app/services/characteristics_service.py
from app.db.repos.characteristics_repository import CharacteristicsRepository
from app.schemas.characteristics_schemas import (
    CharacteristicsSheetCreate,
    CharacteristicsSheetResponse,
)


class CharacteristicsService:
    def __init__(self):
        self.characteristics_repo = None

    def set_repository(self, characteristics_repo: CharacteristicsRepository):
        self.characteristics_repo = characteristics_repo

    async def create_characteristics(
        self, characteristics_data: CharacteristicsSheetCreate
    ) -> CharacteristicsSheetResponse:
        characteristics = await self.characteristics_repo.create_characteristics(
            characteristics_data
        )
        return CharacteristicsSheetResponse.from_orm(characteristics)

    async def get_characteristics(
        self, characteristics_id: int
    ) -> CharacteristicsSheetResponse | None:
        characteristics = await self.characteristics_repo.get_characteristics_by_id(
            characteristics_id
        )
        if not characteristics:
            return None
        return CharacteristicsSheetResponse.from_orm(characteristics)

    async def update_characteristics(
        self, characteristics_id: int, characteristics_data: CharacteristicsSheetCreate
    ) -> CharacteristicsSheetResponse | None:
        characteristics = await self.characteristics_repo.update_characteristics(
            characteristics_id, characteristics_data
        )
        if not characteristics:
            return None
        return CharacteristicsSheetResponse.from_orm(characteristics)

    async def delete_characteristics(self, characteristics_id: int) -> bool:
        return await self.characteristics_repo.delete_characteristics(
            characteristics_id
        )
