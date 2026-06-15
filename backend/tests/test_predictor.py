from app.schemas.analytics import PerformanceMetrics


def test_predictor_generates_cluster_and_persists_model(predictor):
    metrics = PerformanceMetrics(
        kills=20,
        deaths=15,
        assists=7,
        headshots=10,
        adr=80.0,
        kast=70.0,
        rating=1.05,
    )

    first = predictor.predict(metrics)
    second = predictor.predict(metrics)

    assert first.cluster_id == second.cluster_id
    assert first.cluster_label == second.cluster_label
    assert predictor.model_path.exists()
