from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert "message" in r.json()
    assert r.json()["message"] == "ok!"
