import enum

from sqlalchemy import Integer, Column, String, Enum

from app.db.db_vitals import Base
from app.db.models.enums.ability import Ability
from app.db.models.enums.dice_type import DiceType


class ArmorTypeEnum(enum.Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    SHIELD = "Shield"
    NONE = "None"


class CharacterClass(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    hit_dice = Column(Enum(DiceType, name='hit_dice_enum', create_type=False), nullable=False)
    primary_ability = Column(Enum(Ability, name='ability_enum', create_type=True), nullable=False)
    starting_gold = Column(Integer, default=0)
    saving_throw_1 = Column(Enum(Ability, name='st_enum_1', create_type=False), nullable=False)
    saving_throw_2 = Column(Enum(Ability, name='st_enum_2', create_type=False), nullable=False)
    armor_proficiency = Column(Enum(ArmorTypeEnum, name='armor_type_enum', create_type=True), nullable=False, default=ArmorTypeEnum.NONE)

    def __repr__(self):
        return f"<CharacterClass(Name='{self.name}', HitDice='{self.hit_dice.name}')>"