def test_health(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert "response_time_ms" in data
    assert "data_freshness_timestamp" in data
    assert data["data"]["status"] == "ok"