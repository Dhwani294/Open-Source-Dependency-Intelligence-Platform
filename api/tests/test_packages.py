def test_package_risk(client):
    response = client.get("/api/v1/packages/requests")

    assert response.status_code == 200

    data = response.json()

    assert "risk_score" in data["data"]
    assert data["data"]["package_name"] == "requests"
    assert data["data"]["vulnerability_count"] >= 0