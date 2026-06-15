from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.v1 import api_v1_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok", "docs": "/api/docs"}


@app.get("/api/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
