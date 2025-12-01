from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routes.campaign_routes import router

app = FastAPI(title="Campaign Service", root_path="/api/v1", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Campaign Service is running"}
