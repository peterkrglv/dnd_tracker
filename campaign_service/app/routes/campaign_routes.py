from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.campaign_service import CampaignService
from app.config.dependencies import get_campaign_service, get_current_user_id
from app.db.models.enums import UserStatus
from app.schemas.campaign_schemas import (
    Campaign,
    CampaignCreate,
    CampaignDetail,
    CampaignListElement,
    CampaignUpdate,
    Note,
    NoteCreate,
    NoteUpdate,
)

router = APIRouter(prefix="/campaign", tags=["campaign"])


@router.post(
    "/", response_model=CampaignListElement, status_code=status.HTTP_201_CREATED
)
async def create_campaign(
    campaign_data: CampaignCreate,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    campaign = await campaign_service.create_campaign(user_id, campaign_data)
    response_data = Campaign.model_validate(campaign).model_dump()
    response_data["is_master"] = True
    return response_data


@router.get("/", response_model=list[CampaignListElement])
async def get_user_campaigns(
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    campaigns = await campaign_service.get_user_campaigns(user_id)
    response_data = []
    for campaign in campaigns:
        campaign_dict = Campaign.model_validate(campaign).model_dump()

        user_association = next(
            (assoc for assoc in campaign.user_associations if assoc.user_id == user_id),
            None,
        )

        is_master = (
            user_association is not None
            and user_association.status == UserStatus.MASTER
        )

        campaign_dict["is_master"] = is_master
        response_data.append(campaign_dict)
    return response_data


@router.get("/{campaign_id}", response_model=CampaignDetail)
async def get_campaign_details(
    campaign_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    return await campaign_service.get_campaign_details(campaign_id, user_id)


@router.put("/{campaign_id}", response_model=CampaignListElement)
async def update_campaign(
    campaign_id: UUID,
    campaign_data: CampaignUpdate,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    campaign = await campaign_service.update_campaign(
        campaign_id, user_id, campaign_data
    )
    response_data = Campaign.model_validate(campaign).model_dump()
    response_data["is_master"] = True
    return response_data


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    await campaign_service.delete_campaign(campaign_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{campaign_id}/join", status_code=status.HTTP_200_OK)
async def join_campaign(
    campaign_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    await campaign_service.join_campaign(campaign_id, user_id)
    return {"message": "Successfully joined campaign"}


@router.post(
    "/{campaign_id}/note", response_model=Note, status_code=status.HTTP_201_CREATED
)
async def create_note(
    campaign_id: UUID,
    note_data: NoteCreate,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    return await campaign_service.create_note(campaign_id, user_id, note_data)


@router.get("/{campaign_id}/note", response_model=list[Note])
async def get_campaign_notes(
    campaign_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    return await campaign_service.get_campaign_notes(campaign_id, user_id)


@router.get("/{campaign_id}/note/{note_id}", response_model=Note)
async def get_note_details(
    note_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    return await campaign_service.get_note_details(note_id, user_id)


@router.put("/{campaign_id}/note/{note_id}", response_model=Note)
async def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    return await campaign_service.update_note(note_id, user_id, note_data)


@router.delete("/{campaign_id}/note/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    campaign_service: CampaignService = Depends(get_campaign_service),
):
    await campaign_service.delete_note(note_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
