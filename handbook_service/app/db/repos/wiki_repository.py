import uuid
from typing import List, Optional

from pymongo.database import Database

from app.schemas.wiki_schemas import WikiItem, WikiItemCreate, WikiItemDetail


def _map_doc_to_item(doc: dict) -> dict:
    if not doc:
        return {}
    return {
        "uuid": str(doc.get("_id")),
        "title": doc.get("title"),
        "tag": doc.get("tag"),
        "content": doc.get("content"),
        "description": doc.get("description"),
    }


class WikiRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.get_collection("wiki")

    def get_all(self) -> List[WikiItem]:
        cursor = self.collection.find()
        return [WikiItem(**_map_doc_to_item(doc)) for doc in cursor]

    def get_by_id(self, item_id: str) -> Optional[WikiItemDetail]:
        doc = self.collection.find_one({"_id": item_id})
        mapped = _map_doc_to_item(doc)
        return WikiItemDetail(**mapped) if mapped else None

    def find_by_tag(self, tag: str) -> List[WikiItem]:
        cursor = self.collection.find({"tag": tag})
        return [WikiItem(**_map_doc_to_item(doc)) for doc in cursor]

    def search_by_title(self, title: str) -> List[WikiItem]:
        cursor = self.collection.find({"title": {"$regex": title, "$options": "i"}})
        return [WikiItem(**_map_doc_to_item(doc)) for doc in cursor]

    def search_by_content(self, content: str) -> List[WikiItem]:
        cursor = self.collection.find({"content": {"$regex": content, "$options": "i"}})
        return [WikiItem(**_map_doc_to_item(doc)) for doc in cursor]

    def create(self, item: WikiItemCreate) -> WikiItem:
        item_dict = item.dict()
        item_dict.setdefault("_id", str(uuid.uuid4()))
        self.collection.insert_one(item_dict)
        created_item = self.collection.find_one({"_id": item_dict["_id"]})
        return WikiItem(**_map_doc_to_item(created_item))
