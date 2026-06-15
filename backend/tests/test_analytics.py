def test_predict_endpoint_returns_cluster(client):
    payload = {
        "kills": 24,
        "deaths": 16,
        "assists": 6,
        "headshots": 14,
        "adr": 92.3,
        "kast": 78.0,
        "rating": 1.25,
    }

    response = client.post("/api/v1/analytics/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "cluster_id" in data
    assert isinstance(data["cluster_id"], int)
    assert data["cluster_label"]
    assert data["analytical_feedback"]
    assert 0.0 <= data["confidence_score"] <= 1.0
    assert len(data["pca_components"]) == 3
    assert data["feature_vector"] == [
        "kills",
        "deaths",
        "assists",
        "headshots",
        "adr",
        "kast",
        "rating",
    ]


def test_predict_endpoint_validates_negative_kills(client):
    payload = {
        "kills": -1,
        "deaths": 10,
        "assists": 2,
        "headshots": 5,
        "adr": 70.0,
        "kast": 60.0,
        "rating": 0.9,
    }

    response = client.post("/api/v1/analytics/predict", json=payload)
    assert response.status_code == 422
