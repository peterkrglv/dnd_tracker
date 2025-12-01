from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.campaign import (
    Campaign,
    CharacterInCampaign,
    Note,
    Summary,
    UserInCampaign,
)
from app.db.models.enums import UserStatus


class CampaignRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_campaign(
        self, name: str, description: str | None = None, icon_url: str | None = None
    ) -> Campaign:
        campaign = Campaign(name=name, description=description, icon_url=icon_url)
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign

    async def get_campaign_by_id(self, campaign_id: UUID) -> Campaign | None:
        return await self.db.get(Campaign, campaign_id)

    async def get_campaigns_by_user_id(self, user_id: UUID) -> list[Campaign]:
        result = await self.db.execute(
            select(Campaign)
            .join(UserInCampaign)
            .where(UserInCampaign.user_id == user_id)
            .options(joinedload(Campaign.user_associations))
        )
        return result.scalars().unique().all()

    async def update_campaign(
        self, campaign_id: UUID, update_data: dict
    ) -> Campaign | None:
        campaign = await self.get_campaign_by_id(campaign_id)
        if not campaign:
            return None

        for key, value in update_data.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)

        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign

    async def delete_campaign(self, campaign_id: UUID) -> bool:
        campaign = await self.get_campaign_by_id(campaign_id)
        if not campaign:
            return False
        await self.db.delete(campaign)
        await self.db.commit()
        return True

    async def add_user_to_campaign(
        self, campaign_id: UUID, user_id: UUID, status: UserStatus
    ) -> UserInCampaign:
        association = UserInCampaign(
            campaign_id=campaign_id, user_id=user_id, status=status
        )
        self.db.add(association)
        await self.db.commit()
        await self.db.refresh(association)
        return association

    async def get_users_in_campaign(self, campaign_id: UUID) -> list[UserInCampaign]:
        result = await self.db.execute(
            select(UserInCampaign).where(UserInCampaign.campaign_id == campaign_id)
        )
        return result.scalars().all()

    async def remove_user_from_campaign(self, campaign_id: UUID, user_id: UUID) -> bool:
        stmt = delete(UserInCampaign).where(
            UserInCampaign.campaign_id == campaign_id,
            UserInCampaign.user_id == user_id,
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def add_character_to_campaign(
        self, campaign_id: UUID, character_id: UUID
    ) -> CharacterInCampaign:
        association = CharacterInCampaign(
            campaign_id=campaign_id, character_id=character_id
        )
        self.db.add(association)
        await self.db.commit()
        await self.db.refresh(association)
        return association

    async def remove_character_from_campaign(
        self, campaign_id: UUID, character_id: UUID
    ) -> bool:
        stmt = delete(CharacterInCampaign).where(
            CharacterInCampaign.campaign_id == campaign_id,
            CharacterInCampaign.character_id == character_id,
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def create_summary(
        self, campaign_id: UUID, title: str, content: str, date: datetime
    ) -> Summary:
        summary = Summary(
            campaign_id=campaign_id, title=title, content=content, date=date
        )
        self.db.add(summary)
        await self.db.commit()
        await self.db.refresh(summary)
        return summary

    async def get_summaries_for_campaign(self, campaign_id: UUID) -> list[Summary]:
        result = await self.db.execute(
            select(Summary).where(Summary.campaign_id == campaign_id)
        )
        return result.scalars().all()

    async def get_notes_for_campaign(
        self, campaign_id: UUID, user_id: UUID
    ) -> list[Note]:
        result = await self.db.execute(
            select(Note).where(
                Note.campaign_id == campaign_id,
                or_(Note.private == False, Note.author_id == user_id),
            )
        )
        return result.scalars().all()

    async def create_note(
        self, campaign_id: UUID, author_id: UUID, title: str, content: str, **kwargs
    ) -> Note:
        note = Note(
            campaign_id=campaign_id,
            author_id=author_id,
            title=title,
            content=content,
            **kwargs,
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_note_by_id(self, note_id: UUID) -> Note | None:
        return await self.db.get(Note, note_id)

    async def update_note(self, note_id: UUID, update_data: dict) -> Note | None:
        note = await self.get_note_by_id(note_id)
        if not note:
            return None

        for key, value in update_data.items():
            if hasattr(note, key):
                setattr(note, key, value)

        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def delete_note(self, note_id: UUID) -> bool:
        note = await self.get_note_by_id(note_id)
        if not note:
            return False
        await self.db.delete(note)
        await self.db.commit()
        return True
