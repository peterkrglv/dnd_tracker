from pymongo.database import Database
from typing import Optional
from app.schemas.setting_schemas import Setting, SettingCreate, SettingUpdate, NPCCreate
import uuid


class SettingRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.get_collection("settings")

    def create(self, data: SettingCreate) -> Setting:
        doc = data.model_dump()
        doc.setdefault("_id", str(uuid.uuid4()))
        self.collection.insert_one(doc)
        created = self.collection.find_one({"_id": doc["_id"]})
        return Setting(
            uuid=str(created.get("_id")),
            campaign_uuid=created.get("campaign_uuid"),
            lore=created.get("lore"),
            setting=created.get("setting"),
            npcs=created.get("npcs", []),
        )

    def get_by_campaign(self, campaign_uuid: str) -> Optional[Setting]:
        doc = self.collection.find_one({"campaign_uuid": campaign_uuid})
        if not doc:
            return None
        return Setting(
            uuid=str(doc.get("_id")),
            campaign_uuid=doc.get("campaign_uuid"),
            lore=doc.get("lore"),
            setting=doc.get("setting"),
            npcs=doc.get("npcs", []),
        )

    def update(self, campaign_uuid: str, data: SettingUpdate) -> Optional[Setting]:
        self.collection.update_one({"campaign_uuid": campaign_uuid}, {"$set": data.model_dump(exclude_none=True)})
        return self.get_by_campaign(campaign_uuid)

    def delete(self, campaign_uuid: str) -> None:
        self.collection.delete_one({"campaign_uuid": campaign_uuid})

    def add_npc(self, campaign_uuid: str, npc: NPCCreate) -> dict:
        npc_doc = npc.model_dump()
        self.collection.update_one({"campaign_uuid": campaign_uuid}, {"$push": {"npcs": npc_doc}}, upsert=True)
        return npc_doc
