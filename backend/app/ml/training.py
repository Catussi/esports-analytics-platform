from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from app.ml.constants import (
    ARCHETYPE_TEMPLATES,
    DEFAULT_N_CLUSTERS,
    DEFAULT_PCA_COMPONENTS,
    FEATURE_NAMES,
)


def extract_feature_matrix(dataframe: pd.DataFrame) -> np.ndarray:
    return dataframe[FEATURE_NAMES].to_numpy(dtype=np.float64)


def build_cluster_profiles(
    dataframe: pd.DataFrame,
    labels: np.ndarray,
    n_clusters: int = DEFAULT_N_CLUSTERS,
) -> dict[int, dict[str, str]]:
    cluster_means: list[tuple[int, pd.Series]] = []
    for cluster_id in range(n_clusters):
        mask = labels == cluster_id
        means = dataframe.loc[mask, FEATURE_NAMES].mean()
        cluster_means.append((cluster_id, means))

    cluster_means.sort(key=lambda item: item[1]["kills"], reverse=True)

    profiles: dict[int, dict[str, str]] = {}
    for rank, (cluster_id, means) in enumerate(cluster_means):
        template = ARCHETYPE_TEMPLATES[rank % len(ARCHETYPE_TEMPLATES)]
        profiles[cluster_id] = {
            "label": template["label"],
            "feedback": template["feedback"].format(
                kills=means["kills"],
                deaths=means["deaths"],
                assists=means["assists"],
                headshots=means["headshots"],
                adr=means["adr"],
                kast=means["kast"],
                rating=means["rating"],
            ),
        }

    return profiles


def train_clustering_pipeline(
    dataframe: pd.DataFrame,
    n_clusters: int = DEFAULT_N_CLUSTERS,
    n_components: int = DEFAULT_PCA_COMPONENTS,
    random_state: int = 42,
) -> dict:
    if len(dataframe) < n_clusters:
        raise ValueError(
            f"Se requieren al menos {n_clusters} registros para entrenar; recibidos: {len(dataframe)}."
        )

    features = extract_feature_matrix(dataframe)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    pca = PCA(n_components=n_components, random_state=random_state)
    reduced = pca.fit_transform(scaled)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(reduced)

    profiles = build_cluster_profiles(dataframe, labels, n_clusters=n_clusters)

    return {
        "scaler": scaler,
        "pca": pca,
        "kmeans": kmeans,
        "feature_names": FEATURE_NAMES,
        "cluster_profiles": profiles,
        "training_samples": len(dataframe),
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
    }


def save_pipeline(pipeline: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path)
    return output_path
