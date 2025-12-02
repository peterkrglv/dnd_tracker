from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserCharacterAssociation(Base):
    __tablename__ = "users_characters"

    user_uuid = Column(UUID(as_uuid=True), primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)

    def __repr__(self):
        return f"<UserCharacterAssociation(user_uuid='{self.user_uuid}', char_id={self.character_id})>"
