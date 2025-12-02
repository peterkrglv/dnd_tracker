import enum

from sqlalchemy import Column, Enum, Integer, String, Text

from app.db.db_vitals import Base
from app.db.models.enums.source import Source


class SizeEnum(enum.Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class Race(Base):
    __tablename__ = "races"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    source = Column(
        Enum(Source, name="source", create_type=True), index=True, nullable=False
    )
    abilities = Column(Text)
    appearance = Column(Text)
    description = Column(Text)
    languages = Column(String(255))
    max_lifespan = Column(Integer)
    size = Column(Enum(SizeEnum, name="size", create_type=True), nullable=False)
    speed_ft = Column(Integer)

    def __repr__(self):
        return (
            f"<Race(id={self.id}, name='{self.name}', source='{self.source.value}', "
            f"size='{self.size.value}', speed={self.speed_ft})>"
        )
