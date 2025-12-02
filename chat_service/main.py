import uvicorn
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from chat_service.app.routes.chat_routes import router as chat_router
from chat_service.app.config.logging import logger

app = FastAPI(
    title="D&D Chat Service",
    description="Микросервис для чата кампании.",
    version="1.0.0",
)

app.add_middleware(CorrelationIdMiddleware)


@app.on_event("startup")
async def startup():
    logger.info("D&D Chat Service started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("D&D Chat Service shutting down")


app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
