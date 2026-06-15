from fastapi import APIRouter

from app.routers.v1 import analytics, players

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(players.router)
api_v1_router.include_router(analytics.router)
