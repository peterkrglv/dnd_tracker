from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from app.db.models.enums.source import Source
from app.db.models.enums.dice_type import DiceType
from app.db.models.enums.ability import Ability
from app.db.models.enums.damage_type import DamageType
from app.db.models.enums.weapon_category import WeaponCategory
from app.db.models.enums.weapon_type import WeaponType
from app.db.models.enums.size import SizeEnum
from app.db.models.enums.armor_mastery import ArmorMasteryEnum


class RaceInfo(BaseModel):
    id: int
    name: str
    source: Source
    abilities: Optional[str] = None
    appearance: Optional[str] = None
    description: Optional[str] = None
    languages: Optional[str] = None
    max_lifespan: Optional[int] = None
    size: SizeEnum
    speed_ft: int


class ClassInfo(BaseModel):
    id: int
    name: str
    source: Source
    description: Optional[str] = None
    hit_dice: DiceType
    main_ability: Optional[Ability] = None
    max_armor_mastery: ArmorMasteryEnum
    proficient_with_shields: bool
    saving_throw_1: Ability
    saving_throw_2: Ability
    starting_skills_count: Optional[int] = None
    weapon_proficiencies: Optional[str] = None


class WeaponInfo(BaseModel):
    id: int
    name: str
    source: Source
    category: WeaponCategory
    damage_dice: str
    damage_dice_type: DiceType
    damage_type: DamageType
    properties: Optional[str] = None
    range_long: Optional[int] = None
    range_normal: Optional[int] = None
    weapon_type: WeaponType
    weight_lb: Optional[int] = None


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
                source=obj.race.source,
                abilities=obj.race.abilities,
                appearance=obj.race.appearance,
                description=obj.race.description,
                languages=obj.race.languages,
                max_lifespan=obj.race.max_lifespan,
                size=obj.race.size,
                speed_ft=obj.race.speed_ft
            ) if obj.race else None,
            race_secondary=RaceInfo(
                id=obj.race_secondary.id,
                name=obj.race_secondary.name,
                source=obj.race_secondary.source,
                abilities=obj.race_secondary.abilities,
                appearance=obj.race_secondary.appearance,
                description=obj.race_secondary.description,
                languages=obj.race_secondary.languages,
                max_lifespan=obj.race_secondary.max_lifespan,
                size=obj.race_secondary.size,
                speed_ft=obj.race_secondary.speed_ft
            ) if obj.race_secondary else None,
            char_class=ClassInfo(
                id=obj.char_class.id,
                name=obj.char_class.name,
                source=obj.char_class.source,
                description=obj.char_class.description,
                hit_dice=obj.char_class.hit_dice,
                main_ability=obj.char_class.main_ability,
                max_armor_mastery=obj.char_class.max_armor_mastery,
                proficient_with_shields=obj.char_class.proficient_with_shields,
                saving_throw_1=obj.char_class.saving_throw_1,
                saving_throw_2=obj.char_class.saving_throw_2,
                starting_skills_count=obj.char_class.starting_skills_count,
                weapon_proficiencies=obj.char_class.weapon_proficiencies
            ) if obj.char_class else None,
            char_class_secondary=ClassInfo(
                id=obj.char_class_secondary.id,
                name=obj.char_class_secondary.name,
                source=obj.char_class_secondary.source,
                description=obj.char_class_secondary.description,
                hit_dice=obj.char_class_secondary.hit_dice,
                main_ability=obj.char_class_secondary.main_ability,
                max_armor_mastery=obj.char_class_secondary.max_armor_mastery,
                proficient_with_shields=obj.char_class_secondary.proficient_with_shields,
                saving_throw_1=obj.char_class_secondary.saving_throw_1,
                saving_throw_2=obj.char_class_secondary.saving_throw_2,
                starting_skills_count=obj.char_class_secondary.starting_skills_count,
                weapon_proficiencies=obj.char_class_secondary.weapon_proficiencies
            ) if obj.char_class_secondary else None,
            weapons=[
                WeaponInfo(
                    id=weapon.id,
                    name=weapon.name,
                    source=weapon.source,
                    category=weapon.category,
                    damage_dice=weapon.damage_dice,
                    damage_dice_type=weapon.damage_dice_type,
                    damage_type=weapon.damage_type,
                    properties=weapon.properties,
                    range_long=weapon.range_long,
                    range_normal=weapon.range_normal,
                    weapon_type=weapon.weapon_type,
                    weight_lb=weapon.weight_lb
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