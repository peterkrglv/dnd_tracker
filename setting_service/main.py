import uvicorn
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from app.routes.setting_routes import router as setting_router
from app.config.logging import logger

app = FastAPI(
    title="D&D Setting Service",
    description="Микросервис для управления сеттингом кампании и NPC.",
    version="1.0.0",
)

app.add_middleware(CorrelationIdMiddleware)


@app.on_event("startup")
async def startup():
    logger.info("D&D Setting Service started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("D&D Setting Service shutting down")


app.include_router(setting_router, prefix="/api/v1/setting", tags=["setting"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
def main():
    print("Hello from setting-service!")


if __name__ == "__main__":
    main()
