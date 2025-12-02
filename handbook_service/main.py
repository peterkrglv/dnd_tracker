import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config.logging import logger
from app.routes.wiki_routes import router as wiki_router

app = FastAPI(
    title="D&D Wiki Service",
    description="Микросервис справочника (Wiki).",
    version="1.0.0",
)

app.add_middleware(CorrelationIdMiddleware)


@app.on_event("startup")
async def startup():
    logger.info("D&D Wiki Service started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("D&D Wiki Service shutting down")


app.include_router(wiki_router, prefix="/api/v1/wiki", tags=["wiki"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("servers", [{"url": "http://localhost:8082"}])
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
