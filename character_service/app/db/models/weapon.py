import enum

from sqlalchemy import Column, Enum, Integer, String, Text

from app.db.db_vitals import Base
from app.db.models.enums.dice_type import DiceType
from app.db.models.enums.source import Source


class DamageType(enum.Enum):
    SLASHING = "Slashing"
    PIERCING = "Piercing"
    BLUDGEONING = "Bludgeoning"


class WeaponCategory(enum.Enum):
    SIMPLE = "Simple"
    MARTIAL = "Martial"


class WeaponType(enum.Enum):
    MELEE = "Melee"
    RANGED = "Ranged"


class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    source = Column(
        Enum(Source, name="source", create_type=True),
        index=True,
        nullable=False,
    )

    category = Column(
        Enum(WeaponCategory, name="weapon_category", create_type=True), nullable=False
    )
    damage_dice = Column(String(10), nullable=False)
    damage_dice_type = Column(
        Enum(DiceType, name="damage_dice", create_type=True), nullable=False
    )
    damage_type = Column(
        Enum(DamageType, name="damage_type", create_type=True), nullable=False
    )
    properties = Column(Text)
    range_long = Column(Integer)
    range_normal = Column(Integer)
    weapon_type = Column(
        Enum(WeaponType, name="weapon_type", create_type=True), nullable=False
    )
    weight_lb = Column(Integer)

    def __repr__(self):
        return (
            f"<Weapon(name='{self.name}', Damage='{self.damage_dice} {self.damage_type.value}', "
            f"Category='{self.category.value}')>"
        )
