from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_vitals import get_async_session
from app.db.repos.user_repository import UserRepository
from app.user_service import UserService

security = HTTPBearer()


async def get_user_service(
    db: AsyncSession = Depends(get_async_session),
) -> UserService:
    user_service = UserService()
    user_service.set_repository(UserRepository(db))
    return user_service


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_current_user(credentials.credentials)
