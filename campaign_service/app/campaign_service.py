from uuid import UUID

from fastapi import HTTPException, status

from app.db.models.enums import UserStatus
from app.db.repos.campaign_repository import CampaignRepository
from app.schemas.campaign_schemas import (
    CampaignCreate,
    CampaignUpdate,
    NoteCreate,
    NoteUpdate,
)


class CampaignService:
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo

    async def _is_user_master(self, campaign_id: UUID, user_id: UUID) -> bool:
        users = await self.campaign_repo.get_users_in_campaign(campaign_id)
        for u in users:
            if u.user_id == user_id and u.status == UserStatus.MASTER:
                return True
        return False

    async def _user_has_access(self, campaign_id: UUID, user_id: UUID) -> bool:
        users = await self.campaign_repo.get_users_in_campaign(campaign_id)
        return any(u.user_id == user_id for u in users)

    async def create_campaign(self, user_id: UUID, campaign_data: CampaignCreate):
        campaign = await self.campaign_repo.create_campaign(
            **campaign_data.model_dump()
        )
        await self.campaign_repo.add_user_to_campaign(
            campaign.id, user_id, UserStatus.MASTER
        )
        return campaign

    async def get_user_campaigns(self, user_id: UUID):
        return await self.campaign_repo.get_campaigns_by_user_id(user_id)

    async def get_campaign_details(self, campaign_id: UUID, user_id: UUID):
        if not await self._user_has_access(campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        campaign = await self.campaign_repo.get_campaign_by_id(campaign_id)
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
            )

        # Here we would ideally fetch user details from the user_service
        # For now, we return placeholder data.
        users_in_campaign = await self.campaign_repo.get_users_in_campaign(campaign_id)
        participants = [
            {"id": u.user_id, "username": f"user_{u.user_id.hex[:6]}"}
            for u in users_in_campaign
        ]

        notes = await self.campaign_repo.get_notes_for_campaign(campaign_id, user_id)

        campaign_details = campaign.__dict__
        campaign_details["participants"] = participants
        campaign_details["notes"] = notes
        return campaign_details

    async def update_campaign(
        self, campaign_id: UUID, user_id: UUID, campaign_data: CampaignUpdate
    ):
        if not await self._is_user_master(campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only masters can update campaign",
            )

        updated_campaign = await self.campaign_repo.update_campaign(
            campaign_id, campaign_data.model_dump(exclude_unset=True)
        )
        if not updated_campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
            )
        return updated_campaign

    async def delete_campaign(self, campaign_id: UUID, user_id: UUID):
        if not await self._is_user_master(campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only masters can delete campaign",
            )

        if not await self.campaign_repo.delete_campaign(campaign_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
            )

    async def join_campaign(self, campaign_id: UUID, user_id: UUID):
        if await self._user_has_access(campaign_id, user_id):
            # Or maybe return a 200 OK without changes
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in campaign",
            )

        campaign = await self.campaign_repo.get_campaign_by_id(campaign_id)
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
            )

        await self.campaign_repo.add_user_to_campaign(
            campaign.id, user_id, UserStatus.PLAYER
        )

    async def create_note(
        self, campaign_id: UUID, user_id: UUID, note_data: NoteCreate
    ):
        if not await self._user_has_access(campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        return await self.campaign_repo.create_note(
            campaign_id=campaign_id, author_id=user_id, **note_data.model_dump()
        )

    async def get_campaign_notes(self, campaign_id: UUID, user_id: UUID):
        if not await self._user_has_access(campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return await self.campaign_repo.get_notes_for_campaign(campaign_id, user_id)

    async def get_note_details(self, note_id: UUID, user_id: UUID):
        # This is inefficient, should be a single query in a real app
        note = await self.campaign_repo.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        if not await self._user_has_access(note.campaign_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        if note.private and note.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="This note is private"
            )

        return note

    async def update_note(self, note_id: UUID, user_id: UUID, note_data: NoteUpdate):
        note = await self.campaign_repo.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        if note.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the author can update their note",
            )

        return await self.campaign_repo.update_note(
            note_id, note_data.model_dump(exclude_unset=True)
        )

    async def delete_note(self, note_id: UUID, user_id: UUID):
        note = await self.campaign_repo.get_note_by_id(note_id)
        if not note:
            # To prevent leaking information, we might just return success
            # but for development, explicit is better.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        is_master = await self._is_user_master(note.campaign_id, user_id)
        if note.author_id != user_id and not is_master:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the author or a master can delete this note",
            )

        if not await self.campaign_repo.delete_note(note_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
