from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.characteristics_sheet import CharacteristicSheet
from app.schemas.characteristics_schemas import CharacteristicsSheetCreate


class CharacteristicsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_characteristics(
        self, characteristics_data: CharacteristicsSheetCreate
    ) -> CharacteristicSheet:
        characteristics = CharacteristicSheet(
            str_score=characteristics_data.str_score,
            dex_score=characteristics_data.dex_score,
            con_score=characteristics_data.con_score,
            int_score=characteristics_data.int_score,
            wis_score=characteristics_data.wis_score,
            cha_score=characteristics_data.cha_score,
        )
        self.db.add(characteristics)
        await self.db.commit()
        await self.db.refresh(characteristics)
        return characteristics

    async def get_characteristics_by_id(
        self, characteristics_id: int
    ) -> CharacteristicSheet | None:
        result = await self.db.execute(
            select(CharacteristicSheet).where(
                CharacteristicSheet.id == characteristics_id
            )
        )
        return result.scalar_one_or_none()

    async def update_characteristics(
        self, characteristics_id: int, characteristics_data: CharacteristicsSheetCreate
    ) -> CharacteristicSheet | None:
        characteristics = await self.get_characteristics_by_id(characteristics_id)
        if not characteristics:
            return None

        for field, value in characteristics_data.dict(exclude_unset=True).items():
            setattr(characteristics, field, value)

        await self.db.commit()
        await self.db.refresh(characteristics)
        return characteristics

    async def delete_characteristics(self, characteristics_id: int) -> bool:
        characteristics = await self.get_characteristics_by_id(characteristics_id)
        if not characteristics:
            return False

        await self.db.delete(characteristics)
        await self.db.commit()
        return True
