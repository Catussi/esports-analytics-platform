from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from app.config import get_settings
from app.ml.constants import FALLBACK_CLUSTER_PROFILES, FEATURE_NAMES
from app.schemas.analytics import PerformanceMetrics, PredictionResponse


class ClusterPredictor:
    """Carga un modelo pre-entrenado (.joblib) para inferencia de clústeres."""

    def __init__(self, model_path: str | None = None) -> None:
        settings = get_settings()
        self.model_path = Path(model_path or settings.ml_model_path)
        self._pipeline: dict | None = None

    def _metrics_to_array(self, metrics: PerformanceMetrics) -> np.ndarray:
        return np.array(
            [
                [
                    metrics.kills,
                    metrics.deaths,
                    metrics.assists,
                    metrics.headshots,
                    metrics.adr,
                    metrics.kast,
                    metrics.rating,
                ]
            ],
            dtype=np.float64,
        )

    def _load_pipeline(self) -> dict:
        if self._pipeline is not None:
            return self._pipeline

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en {self.model_path}. "
                "Ejecuta: python -m scripts.train_model"
            )

        self._pipeline = joblib.load(self.model_path)
        return self._pipeline

    def _distance_confidence(self, point: np.ndarray, centroid: np.ndarray) -> float:
        distance = float(np.linalg.norm(point - centroid))
        return round(max(0.55, 1.0 - (distance / 4.0)), 4)

    def predict(self, metrics: PerformanceMetrics) -> PredictionResponse:
        pipeline = self._load_pipeline()
        scaler: StandardScaler = pipeline["scaler"]
        pca: PCA = pipeline["pca"]
        kmeans: KMeans = pipeline["kmeans"]
        profiles: dict[int, dict[str, str]] = pipeline.get(
            "cluster_profiles",
            FALLBACK_CLUSTER_PROFILES,
        )

        raw = self._metrics_to_array(metrics)
        scaled = scaler.transform(raw)
        reduced = pca.transform(scaled)
        cluster_id = int(kmeans.predict(reduced)[0])
        centroid = kmeans.cluster_centers_[cluster_id]
        profile = profiles.get(
            cluster_id,
            {
                "label": f"Cluster {cluster_id}",
                "feedback": "Perfil de rendimiento identificado por el modelo de clustering.",
            },
        )

        return PredictionResponse(
            cluster_id=cluster_id,
            cluster_label=profile["label"],
            analytical_feedback=profile["feedback"],
            confidence_score=self._distance_confidence(reduced[0], centroid),
            pca_components=[round(float(value), 4) for value in reduced[0]],
            feature_vector=FEATURE_NAMES,
        )


_predictor: ClusterPredictor | None = None


def get_predictor() -> ClusterPredictor:
    global _predictor
    if _predictor is None:
        _predictor = ClusterPredictor()
    return _predictor


def reset_predictor() -> None:
    global _predictor
    _predictor = None
