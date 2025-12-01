import uuid

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.db_vitals import Base
from app.db.models.enums import user_status_enum


class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)

    summaries = relationship(
        "Summary", back_populates="campaign", cascade="all, delete-orphan"
    )
    notes = relationship(
        "Note", back_populates="campaign", cascade="all, delete-orphan"
    )
    user_associations = relationship(
        "UserInCampaign", back_populates="campaign", cascade="all, delete-orphan"
    )


class Summary(Base):
    __tablename__ = "summaries"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(TIMESTAMP, nullable=False)

    campaign = relationship("Campaign", back_populates="summaries")


class Note(Base):
    __tablename__ = "notes"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)  # FK to user_service.users
    private = Column(Boolean, default=False, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    color = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    date = Column(TIMESTAMP, nullable=False, default=func.now())

    campaign = relationship("Campaign", back_populates="notes")


class CharacterInCampaign(Base):
    __tablename__ = "character_in_campaign"
    __table_args__ = {"extend_existing": True}

    character_id = Column(
        UUID(as_uuid=True), primary_key=True
    )  # FK to character_service.characters
    campaign_id = Column(
        UUID(as_uuid=True), ForeignKey("campaigns.id"), primary_key=True
    )


class UserInCampaign(Base):
    __tablename__ = "user_in_campaign"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(as_uuid=True), primary_key=True)  # FK to user_service.users
    campaign_id = Column(
        UUID(as_uuid=True), ForeignKey("campaigns.id"), primary_key=True
    )
    status = Column(user_status_enum, nullable=False)

    campaign = relationship("Campaign", back_populates="user_associations")
