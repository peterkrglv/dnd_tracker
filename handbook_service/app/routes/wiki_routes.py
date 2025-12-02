from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.config.dependencies import get_handbook_service
from app.handbook_service import HandbookService
from app.schemas.wiki_schemas import WikiItem, WikiItemDetail

router = APIRouter()


@router.get("/", response_model=List[WikiItem])
async def get_wiki_list(
    tag: Optional[str] = None,
    search_title: Optional[str] = None,
    search_content: Optional[str] = None,
    handbook_service: HandbookService = Depends(get_handbook_service),
):
    return await handbook_service.get_wiki_list(tag, search_title, search_content)


@router.get("/{item_id}", response_model=WikiItemDetail)
async def get_wiki_item(
    item_id: str,
    handbook_service: HandbookService = Depends(get_handbook_service),
):
    item = await handbook_service.get_wiki_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
