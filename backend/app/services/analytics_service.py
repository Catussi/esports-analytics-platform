from app.ml.predictor import ClusterPredictor, get_predictor
from app.schemas.analytics import PredictionRequest, PredictionResponse


class AnalyticsService:
    def __init__(self, predictor: ClusterPredictor | None = None) -> None:
        self.predictor = predictor or get_predictor()

    def predict_cluster(self, payload: PredictionRequest) -> PredictionResponse:
        return self.predictor.predict(payload)
