from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routes.user_routes import router

app = FastAPI(title="User Service", root_path="/api/v1/user")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "User Service is running"}
