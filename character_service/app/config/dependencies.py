from uuid import UUID

from app.services.characteristics_service import CharacteristicsService
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.character_service import CharacterService
from app.db.db_vitals import get_async_session
from app.db.repos.character_repository import CharacterRepository
from app.db.repos.characteristics_repository import CharacteristicsRepository
from app.utils.security import get_user_id_from_token

security = HTTPBearer()


async def extract_id_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    token = credentials.credentials
    return get_user_id_from_token(token)


async def get_character_service() -> CharacterService:
    async for session in get_async_session():
        repo = CharacterRepository(session)
        service = CharacterService()
        service.set_repository(repo)
        return service


async def get_characteristics_service() -> CharacteristicsService:
    async for session in get_async_session():
        repo = CharacteristicsRepository(session)
        service = CharacteristicsService()
        service.set_repository(repo)
        return service
