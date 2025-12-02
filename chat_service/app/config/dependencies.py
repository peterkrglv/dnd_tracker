from fastapi import Depends
from pymongo.database import Database

from chat_service.app.db.db_vitals import get_database
from chat_service.app.db.repos.message_repository import MessageRepository
from chat_service.app.chat_service import ChatService


def get_chat_service(
    db: Database = Depends(get_database),
) -> ChatService:
    chat_service = ChatService()
    repo = MessageRepository(db)
    chat_service.set_repository(repo)
    return chat_service
