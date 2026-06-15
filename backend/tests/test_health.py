def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "eSports Analytics Platform" in payload["service"]
