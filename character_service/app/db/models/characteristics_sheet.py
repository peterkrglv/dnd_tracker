from sqlalchemy import Column, Integer

from app.db.db_vitals import Base
from app.db.models.enums.ability import Ability


class CharacteristicSheet(Base):
    __tablename__ = "characteristics_sheets"
    id = Column(Integer, primary_key=True, index=True)
    for member in Ability:
        col_name = f"{member.name.lower()}_score"
        vars()[col_name] = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<CharacteristicsSheet(ID={self.id}, STR={self.str_score}, DEX={self.dex_score})>"
