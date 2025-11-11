from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import auth
from app.config.settings import settings
import uvicorn

app = FastAPI(title="Character Service", root_path=f"/api/v1/character")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Character Service is running"}

