def test_maintainer(client):
    response = client.get("/api/v1/maintainers/johndoe")

    assert response.status_code == 200

    data = response.json()

    assert "package_count" in data["data"]
    assert data["data"]["maintainer"] == "johndoe"