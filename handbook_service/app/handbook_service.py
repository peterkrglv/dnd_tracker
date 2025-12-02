from typing import List, Optional

from fastapi.concurrency import run_in_threadpool

from app.db.repos.wiki_repository import WikiRepository
from app.schemas.wiki_schemas import WikiItem, WikiItemCreate, WikiItemDetail


class HandbookService:
    def __init__(self):
        self._repository: Optional[WikiRepository] = None

    def set_repository(self, repository: WikiRepository):
        self._repository = repository

    async def get_wiki_list(
        self,
        tag: Optional[str] = None,
        search_title: Optional[str] = None,
        search_content: Optional[str] = None,
    ) -> List[WikiItem]:
        if tag:
            return await run_in_threadpool(self._repository.find_by_tag, tag)
        if search_title:
            return await run_in_threadpool(
                self._repository.search_by_title, search_title
            )
        if search_content:
            return await run_in_threadpool(
                self._repository.search_by_content, search_content
            )
        return await run_in_threadpool(self._repository.get_all)

    async def get_wiki_item(self, item_id: str) -> Optional[WikiItemDetail]:
        return await run_in_threadpool(self._repository.get_by_id, item_id)

    async def create_wiki_item(self, item: WikiItemCreate) -> WikiItem:
        return await run_in_threadpool(self._repository.create, item)
