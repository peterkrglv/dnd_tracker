from typing import List, Optional
from fastapi.concurrency import run_in_threadpool

from chat_service.app.db.repos.message_repository import MessageRepository
from chat_service.app.schemas.message_schemas import Message, MessageCreate, MessageUpdate


class ChatService:
    def __init__(self):
        self._repository: Optional[MessageRepository] = None

    def set_repository(self, repository: MessageRepository):
        self._repository = repository

    async def post_message(self, campaign_id: str, item: MessageCreate) -> Message:
        return await run_in_threadpool(self._repository.create, campaign_id, item)

    async def get_messages(self, campaign_id: str, page: int = 1, per_page: int = 10) -> List[Message]:
        return await run_in_threadpool(self._repository.list_by_campaign, campaign_id, page, per_page)

    async def get_message(self, campaign_id: str, message_id: str) -> Optional[Message]:
        return await run_in_threadpool(self._repository.get_by_id, campaign_id, message_id)

    async def update_message(self, campaign_id: str, message_id: str, data: MessageUpdate) -> Optional[Message]:
        return await run_in_threadpool(self._repository.update, campaign_id, message_id, data)

    async def delete_message(self, campaign_id: str, message_id: str) -> None:
        return await run_in_threadpool(self._repository.delete, campaign_id, message_id)
