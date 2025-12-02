from typing import Optional
from fastapi.concurrency import run_in_threadpool

from app.db.repos.setting_repository import SettingRepository
from app.schemas.setting_schemas import (
    Setting,
    SettingCreate,
    SettingUpdate,
    NPCCreate,
)


class SettingService:
    def __init__(self):
        self._repository: Optional[SettingRepository] = None

    def set_repository(self, repository: SettingRepository):
        self._repository = repository

    async def create_setting(self, payload: SettingCreate) -> Setting:
        return await run_in_threadpool(self._repository.create, payload)

    async def get_setting(self, campaign_uuid: str) -> Optional[Setting]:
        return await run_in_threadpool(self._repository.get_by_campaign, campaign_uuid)

    async def update_setting(self, campaign_uuid: str, payload: SettingUpdate) -> Optional[Setting]:
        return await run_in_threadpool(self._repository.update, campaign_uuid, payload)

    async def delete_setting(self, campaign_uuid: str) -> None:
        return await run_in_threadpool(self._repository.delete, campaign_uuid)

    async def add_npc(self, campaign_uuid: str, payload: NPCCreate) -> dict:
        return await run_in_threadpool(self._repository.add_npc, campaign_uuid, payload)
