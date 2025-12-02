from pymongo import MongoClient
from pymongo.database import Database

from chat_service.app.config.settings import settings

_client: MongoClient | None = None


def _get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.DATABASE_URL)
    return _client


def get_database() -> Database:
    client = _get_client()
    return client[settings.CHAT_MONGO_DB]
