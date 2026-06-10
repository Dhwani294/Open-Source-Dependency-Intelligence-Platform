def test_ecosystem(client):
    response = client.get("/api/v1/ecosystems/pypi")

    assert response.status_code == 200

    data = response.json()

    assert "avg_severity_score" in data["data"]
    assert data["data"]["ecosystem"] == "pypi"