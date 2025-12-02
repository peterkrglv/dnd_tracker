from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.character import Character
from app.db.models.weapon import Weapon
from app.schemas.character_schemas import CharacterCreate


class CharacterRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_character(
        self, character_data: CharacterCreate, user_id: UUID
    ) -> Character:
        weapons = []
        if character_data.weapon_ids:
            result = await self.db.execute(
                select(Weapon).where(Weapon.id.in_(character_data.weapon_ids))
            )
            weapons = result.scalars().all()

        character = Character(
            name=character_data.name,
            level=character_data.level,
            current_hp=character_data.current_hp,
            max_hp=character_data.max_hp,
            user_id=user_id,
            race_id=character_data.race_id,
            race_id_secondary=character_data.race_id_secondary,
            class_id=character_data.class_id,
            class_id_secondary=character_data.class_id_secondary,
            sheet_id=None,
            weapons=weapons,
        )
        self.db.add(character)
        await self.db.commit()
        await self.db.refresh(character)

        return await self._load_character_relations(character)

    async def get_character_by_id(
        self, character_id: int, user_id: UUID
    ) -> Character | None:
        result = await self.db.execute(
            select(Character)
            .options(
                selectinload(Character.race),
                selectinload(Character.race_secondary),
                selectinload(Character.char_class),
                selectinload(Character.char_class_secondary),
                selectinload(Character.weapons),
            )
            .where(Character.id == character_id, Character.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_character(
        self, character_id: int, character_data: CharacterCreate, user_id: UUID
    ) -> Character | None:
        character = await self.get_character_by_id(character_id, user_id)
        if not character:
            return None

        if character_data.weapon_ids is not None:
            result = await self.db.execute(
                select(Weapon).where(Weapon.id.in_(character_data.weapon_ids))
            )
            character.weapons = result.scalars().all()

        update_data = character_data.dict(exclude={"weapon_ids"}, exclude_unset=True)
        for field, value in update_data.items():
            setattr(character, field, value)

        await self.db.commit()
        await self.db.refresh(character)
        return await self._load_character_relations(character)

    async def delete_character(self, character_id: int, user_id: UUID) -> bool:
        character = await self.get_character_by_id(character_id, user_id)
        if not character:
            return False

        await self.db.delete(character)
        await self.db.commit()
        return True

    async def get_user_characters(self, user_id: UUID) -> list[Character]:
        result = await self.db.execute(
            select(Character)
            .options(
                selectinload(Character.race),
                selectinload(Character.race_secondary),
                selectinload(Character.char_class),
                selectinload(Character.char_class_secondary),
                selectinload(Character.weapons),
            )
            .where(Character.user_id == user_id)
        )
        return result.scalars().all()

    async def set_character_sheet(
        self, character_id: int, sheet_id: int, user_id: UUID
    ) -> bool:
        character = await self.get_character_by_id(character_id, user_id)
        if not character:
            return False

        character.sheet_id = sheet_id
        await self.db.commit()
        return True

    async def _load_character_relations(self, character: Character) -> Character:
        result = await self.db.execute(
            select(Character)
            .options(
                selectinload(Character.race),
                selectinload(Character.race_secondary),
                selectinload(Character.char_class),
                selectinload(Character.char_class_secondary),
                selectinload(Character.weapons),
            )
            .where(Character.id == character.id)
        )
        return result.scalar_one()
