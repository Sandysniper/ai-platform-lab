from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_get_all_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_found():
    response = client.get("/logs/alice")
    assert response.status_code == 200
    assert response.json()["user"] == "alice"


def test_get_user_not_found():
    response = client.get("/logs/zoe")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_log_success():
    new_log = {"user": "Santhosh", "action": "CreateBucket", "status": "SUCCESS"}
    response = client.post("/logs", json=new_log)
    assert response.status_code == 201
    assert response.json()["log_entry"]["user"] == "Santhosh"


def test_create_log_invalid_status():
    bad_log = {"user": "Santhosh", "action": "CreateBucket", "status": "PENDING"}
    response = client.post("/logs", json=bad_log)
    assert response.status_code == 422


def test_create_log_missing_field():
    incomplete_log = {"user": "Santhosh", "action": "CreateBucket"}
    response = client.post("/logs", json=incomplete_log)
    assert response.status_code == 422