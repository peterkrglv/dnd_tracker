from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.db_vitals import Base

character_weapon_association = Table(
    "character_weapon_association",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
    Column("weapon_id", Integer, ForeignKey("weapons.id"), primary_key=True),
)


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    appearance = Column(String(1000))
    current_hp = Column(Integer)
    history = Column(String(1000))
    level = Column(Integer, nullable=False, default=1)
    max_hp = Column(Integer)
    race = relationship("app.db.models.race.Race", foreign_keys=[race_id], backref="primary_characters")
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    race_id_secondary = Column(Integer, ForeignKey("races.id"), nullable=True)
    race_secondary = relationship(
        "app.db.models.race.Race", foreign_keys=[race_id_secondary], backref="secondary_characters"
    )
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    char_class = relationship(
        "app.db.models.class.CharacterClass", foreign_keys=[class_id], backref="primary_class_characters"
    )
    class_id_secondary = Column(Integer, ForeignKey("classes.id"), nullable=True)
    char_class_secondary = relationship(
        "app.db.models.class.CharacterClass",
        foreign_keys=[class_id_secondary],
        backref="secondary_class_characters",
    )
    sheet_id = Column(
        Integer, ForeignKey("characteristics_sheets.id"), unique=True, nullable=False
    )
    characteristics = relationship(
        "app.db.models.characteristic_sheet.CharacteristicSheet", backref="owner", uselist=False
    )
    weapons = relationship(
        "app.db.models.weapon.Weapon",
        secondary=character_weapon_association,
        backref="characters_who_own",
    )

    def __repr__(self):
        race_name = getattr(self.race, "name", "N/A")
        class_name = getattr(self.char_class, "name", "N/A")
        return (
            f"<Character(Name='{self.name}', Lvl={self.level}, "
            f"Race='{race_name}', Class='{class_name}')>"
        )