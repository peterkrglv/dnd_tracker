from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.campaign_service import CampaignService
from app.db.db_vitals import get_async_session
from app.db.repos.campaign_repository import CampaignRepository
from app.utils.security import get_user_id_from_token

security = HTTPBearer()


async def get_campaign_repository(
    db: AsyncSession = Depends(get_async_session),
) -> CampaignRepository:
    return CampaignRepository(db)


async def get_campaign_service(
    repo: CampaignRepository = Depends(get_campaign_repository),
) -> CampaignService:
    return CampaignService(repo)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    user_id = get_user_id_from_token(credentials.credentials)
    return user_id
