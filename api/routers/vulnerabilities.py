def test_vulnerability(client):
    response = client.get("/api/v1/vulnerabilities/OSV-TEST-001")

    assert response.status_code == 200

    data = response.json()

    assert "affected_packages" in data["data"]
    assert "total_affected" in data["data"]