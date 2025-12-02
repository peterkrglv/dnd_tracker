from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status

from chat_service.app.schemas.message_schemas import Message, MessageCreate, MessageUpdate
from chat_service.app.config.dependencies import get_chat_service
from chat_service.app.chat_service import ChatService

router = APIRouter()


@router.post("/{campaign_id}", response_model=Message, status_code=status.HTTP_201_CREATED)
async def post_message(
    campaign_id: str,
    payload: MessageCreate,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.post_message(campaign_id, payload)


@router.get("/{campaign_id}", response_model=List[Message])
async def list_messages(
    campaign_id: str,
    page: Optional[int] = 1,
    per_page: Optional[int] = 10,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.get_messages(campaign_id, page, per_page)


@router.get("/{campaign_id}/{message_id}", response_model=Message)
async def get_message(
    campaign_id: str, message_id: str, chat_service: ChatService = Depends(get_chat_service)
):
    item = await chat_service.get_message(campaign_id, message_id)
    if not item:
        raise HTTPException(status_code=404, detail="Message not found")
    return item


@router.put("/{campaign_id}/{message_id}", response_model=Message)
async def update_message(
    campaign_id: str,
    message_id: str,
    payload: MessageUpdate,
    chat_service: ChatService = Depends(get_chat_service),
):
    item = await chat_service.update_message(campaign_id, message_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Message not found")
    return item


@router.delete("/{campaign_id}/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(campaign_id: str, message_id: str, chat_service: ChatService = Depends(get_chat_service)):
    await chat_service.delete_message(campaign_id, message_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
