from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from dice_service.app.routers.dice_routes import router

import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dice Service",
    description="Microservice for dice rolling operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include routers
app.include_router(router, prefix="/api/v1/dice")

@app.on_event("startup")
async def startup_event():
    logger.info("Dice Service starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Dice Service shutting down...")

@app.get("/")
async def root():
    return {"message": "Dice Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dice"}