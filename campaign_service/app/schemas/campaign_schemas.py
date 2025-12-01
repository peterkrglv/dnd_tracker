from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ======== Base Schemas ========
class CampaignBase(BaseModel):
    name: str
    description: str | None = None


class NoteBase(BaseModel):
    title: str
    content: str
    private: bool = False


# ======== Request Schemas ========
class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    name: str | None = None  # Allow partial updates


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    title: str | None = None
    content: str | None = None
    private: bool | None = None


# ======== Response Schemas ========
class Campaign(CampaignBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class CampaignListElement(Campaign):
    is_master: bool


class Participant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str


class CampaignDetail(Campaign):
    participants: list[Participant]
    notes: list["Note"]  # Forward reference


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    author_id: UUID
    date: datetime
    campaign_id: UUID


# Update forward reference
CampaignDetail.model_rebuild()
