from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Message(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    campaign: str
    created: Optional[str] = None
    updated: Optional[str] = None
    author: Optional[str] = None


class MessageCreate(BaseModel):
    message: str
    author: Optional[str] = None


class MessageUpdate(BaseModel):
    message: str
