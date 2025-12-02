from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class NPC(BaseModel):
    name: str
    description: Optional[str] = None


class Setting(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campaign_uuid: str
    lore: Optional[str] = None
    setting: Optional[str] = None
    npcs: List[NPC] = []


class SettingCreate(BaseModel):
    campaign_uuid: str
    lore: Optional[str] = None
    setting: Optional[str] = None


class SettingUpdate(BaseModel):
    lore: Optional[str] = None
    setting: Optional[str] = None


class NPCCreate(BaseModel):
    name: str
    description: Optional[str] = None
