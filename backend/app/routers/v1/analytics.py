from fastapi import APIRouter

from app.schemas.analytics import PredictionRequest, PredictionResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/predict", response_model=PredictionResponse)
def predict_player_cluster(payload: PredictionRequest) -> PredictionResponse:
    service = AnalyticsService()
    return service.predict_cluster(payload)
