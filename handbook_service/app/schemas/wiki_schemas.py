from typing import Optional

from pydantic import BaseModel


class WikiItem(BaseModel):
    uuid: str
    title: str
    tag: str
    content: Optional[str] = None


class WikiItemDetail(WikiItem):
    description: Optional[str] = None


class WikiItemCreate(BaseModel):
    title: str
    tag: str
    content: str
    description: Optional[str] = None
