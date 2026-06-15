from pydantic import BaseModel, Field


class PerformanceMetrics(BaseModel):
    kills: float = Field(..., ge=0, examples=[22])
    deaths: float = Field(..., ge=0, examples=[18])
    assists: float = Field(..., ge=0, examples=[5])
    headshots: float = Field(..., ge=0, examples=[12])
    adr: float = Field(..., ge=0, examples=[85.4])
    kast: float = Field(..., ge=0, le=100, examples=[72.5])
    rating: float = Field(..., ge=0, examples=[1.12])


class PredictionRequest(PerformanceMetrics):
    """Métricas de rendimiento de un jugador para inferencia de clúster."""


class PredictionResponse(BaseModel):
    cluster_id: int
    cluster_label: str
    analytical_feedback: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    pca_components: list[float]
    feature_vector: list[str]
