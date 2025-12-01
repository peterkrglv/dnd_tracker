from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class RaceInfo(BaseModel):
    id: int
    name: str
    source: str


class ClassInfo(BaseModel):
    id: int
    name: str
    source: str


class WeaponInfo(BaseModel):
    id: int
    name: str
    dice_count: int
    hit_dice: int
    damage_type: str


class CharacterResponse(BaseModel):
    id: int
    name: str
    level: int
    current_hp: Optional[int] = None
    max_hp: Optional[int] = None
    user_id: UUID
    race: RaceInfo
    race_secondary: Optional[RaceInfo] = None
    char_class: ClassInfo
    char_class_secondary: Optional[ClassInfo] = None
    weapons: List[WeaponInfo] = []

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            level=obj.level,
            current_hp=obj.current_hp,
            max_hp=obj.max_hp,
            user_id=obj.user_id,
            race=RaceInfo(
                id=obj.race.id,
                name=obj.race.name,
                source=obj.race.source
            ) if obj.race else None,
            race_secondary=RaceInfo(
                id=obj.race_secondary.id,
                name=obj.race_secondary.name,
                source=obj.race_secondary.source
            ) if obj.race_secondary else None,
            char_class=ClassInfo(
                id=obj.char_class.id,
                name=obj.char_class.name,
                source=obj.char_class.source
            ) if obj.char_class else None,
            char_class_secondary=ClassInfo(
                id=obj.char_class_secondary.id,
                name=obj.char_class_secondary.name,
                source=obj.char_class_secondary.source
            ) if obj.char_class_secondary else None,
            weapons=[
                WeaponInfo(
                    id=weapon.id,
                    name=weapon.name,
                    dice_count=weapon.dice_count,
                    hit_dice=weapon.hit_dice,
                    damage_type=weapon.damage_type
                ) for weapon in obj.weapons
            ] if obj.weapons else []
        )


class CharacterCreate(BaseModel):
    name: str
    level: int = 1
    current_hp: Optional[int] = None
    max_hp: Optional[int] = None
    race_id: int
    race_id_secondary: Optional[int] = None
    class_id: int
    class_id_secondary: Optional[int] = None
    weapon_ids: List[int] = []


class CharacterId(BaseModel):
    id: int