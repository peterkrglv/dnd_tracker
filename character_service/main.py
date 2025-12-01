from app.routers.characteristics_routes import stats_router
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers.character_routes import character_router

app = FastAPI(title="Character Service", root_path="/api/v1/character")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

router = APIRouter(prefix="/api/v1/character")

router.include_router(character_router)
router.include_router(stats_router)

app.include_router(router)


@router.get("/")
async def root():
    return {"message": "Character Service is running"}
