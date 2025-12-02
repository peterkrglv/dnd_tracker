from pymongo import MongoClient
from pymongo.database import Database

from app.config.settings import settings

client = MongoClient(settings.DATABASE_URL)
database = client[settings.HANDBOOK_MONGO_DB]


def get_database() -> Database:
    return database
