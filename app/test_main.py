from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    attributes = ["message", "version"]
    assert all(attr in response.json() for attr in attributes)


def test_musician_route_exists():
    response = client.get("/musicians/")
    assert response.status_code == 200


def test_user_route_exists():
    response = client.get("/users/")
    assert response.status_code == 200


def test_group_route_exists():
    response = client.get("/group/")
    assert response.status_code == 200
