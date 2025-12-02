import uuid
from typing import Optional

from pydantic import BaseModel, Field


class WikiModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str
    tag: str
    content: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Axe",
                "tag": "weapon",
                "content": "A simple axe.",
                "description": "A simple axe that can be used as a tool or a weapon.",
            }
        }
