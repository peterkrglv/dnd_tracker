from pymongo.database import Database
from typing import List, Optional
from chat_service.app.schemas.message_schemas import Message, MessageCreate, MessageUpdate
import uuid


class MessageRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.get_collection("messages")

    def create(self, campaign_id: str, item: MessageCreate) -> Message:
        doc = item.dict()
        doc.setdefault("_id", str(uuid.uuid4()))
        doc["campaign"] = campaign_id
        self.collection.insert_one(doc)
        created = self.collection.find_one({"_id": doc["_id"]})
        return Message(
            uuid=str(created.get("_id")),
            message=created.get("message"),
            campaign=created.get("campaign"),
            author=created.get("author"),
        )

    def list_by_campaign(self, campaign_id: str, page: int = 1, per_page: int = 10) -> List[Message]:
        skip = (page - 1) * per_page
        cursor = self.collection.find({"campaign": campaign_id}).skip(skip).limit(per_page)
        return [Message(uuid=str(d.get("_id")), message=d.get("message"), campaign=d.get("campaign"), author=d.get("author")) for d in cursor]

    def get_by_id(self, campaign_id: str, message_id: str) -> Optional[Message]:
        doc = self.collection.find_one({"_id": message_id, "campaign": campaign_id})
        if not doc:
            return None
        return Message(uuid=str(doc.get("_id")), message=doc.get("message"), campaign=doc.get("campaign"), author=doc.get("author"))

    def update(self, campaign_id: str, message_id: str, data: MessageUpdate) -> Optional[Message]:
        self.collection.update_one({"_id": message_id, "campaign": campaign_id}, {"$set": data.dict()})
        return self.get_by_id(campaign_id, message_id)

    def delete(self, campaign_id: str, message_id: str) -> None:
        self.collection.delete_one({"_id": message_id, "campaign": campaign_id})
