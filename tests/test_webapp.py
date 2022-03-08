def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the sample app" in str(response.data)
    assert "<title>Sample webapp</title>" in str(response.data)
