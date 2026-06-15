import pandas as pd
import pytest

from app.ml.training import build_cluster_profiles, train_clustering_pipeline


def _sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [25, 18, 4, 12, 95.0, 72.0, 1.25],
            [24, 17, 5, 11, 92.0, 74.0, 1.22],
            [23, 19, 3, 10, 90.0, 70.0, 1.18],
            [8, 16, 12, 3, 55.0, 82.0, 0.95],
            [7, 15, 11, 2, 52.0, 80.0, 0.92],
            [9, 17, 10, 4, 58.0, 78.0, 0.98],
            [14, 12, 6, 7, 72.0, 68.0, 1.05],
            [13, 13, 5, 6, 70.0, 66.0, 1.02],
            [15, 11, 7, 8, 75.0, 69.0, 1.08],
            [10, 10, 8, 5, 60.0, 88.0, 1.00],
            [11, 11, 7, 4, 62.0, 85.0, 1.01],
            [9, 12, 9, 3, 58.0, 86.0, 0.99],
        ],
        columns=["kills", "deaths", "assists", "headshots", "adr", "kast", "rating"],
    )


def test_train_clustering_pipeline_structure():
    pipeline = train_clustering_pipeline(_sample_dataframe(), n_clusters=4)

    assert "scaler" in pipeline
    assert "pca" in pipeline
    assert "kmeans" in pipeline
    assert len(pipeline["cluster_profiles"]) == 4
    assert pipeline["training_samples"] == 12


def test_build_cluster_profiles_assigns_unique_labels():
    dataframe = _sample_dataframe()
    pipeline = train_clustering_pipeline(dataframe, n_clusters=4)
    labels = pipeline["kmeans"].labels_

    profiles = build_cluster_profiles(dataframe, labels, n_clusters=4)
    labels_assigned = [profile["label"] for profile in profiles.values()]

    assert len(set(labels_assigned)) == 4
    assert all(profile["feedback"] for profile in profiles.values())
