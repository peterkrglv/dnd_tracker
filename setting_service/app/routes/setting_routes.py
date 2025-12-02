from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.setting_schemas import (
    Setting,
    SettingCreate,
    SettingUpdate,
    NPCCreate,
)
from app.config.dependencies import get_setting_service
from app.setting_service import SettingService

router = APIRouter()


@router.post("", response_model=Setting, status_code=status.HTTP_201_CREATED)
async def create_setting(payload: SettingCreate, svc: SettingService = Depends(get_setting_service)):
    return await svc.create_setting(payload)


@router.get("/campaign/{id}", response_model=Optional[Setting])
async def get_setting(id: str, svc: SettingService = Depends(get_setting_service)):
    return await svc.get_setting(id)


@router.put("/campaign/{id}", response_model=Optional[Setting])
async def update_setting(id: str, payload: SettingUpdate, svc: SettingService = Depends(get_setting_service)):
    item = await svc.update_setting(id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Setting not found")
    return item


@router.delete("/campaign/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(id: str, svc: SettingService = Depends(get_setting_service)):
    await svc.delete_setting(id)
    return None


@router.post("/campaign/{id}/npc", status_code=status.HTTP_201_CREATED)
async def add_npc(id: str, payload: NPCCreate, svc: SettingService = Depends(get_setting_service)):
    npc = await svc.add_npc(id, payload)
    return npc
