from fastapi.testclient import TestClient

from app import app

client = TestClient(app=app)

USER_ATTRS = ["id", "name", "email", "auth0_id"]
BASE_ROUTE = "/users"


def test_user_route_exists():
    response = client.get(BASE_ROUTE)
    assert response.status_code == 200


def test_user_route_details():
    response = client.get(BASE_ROUTE)
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 4

    for user in body:
        assert all(attr in user for attr in USER_ATTRS)


def test_get_user():
    for id_num in range(1, 5):
        response = client.get(f"{BASE_ROUTE}/{id_num}")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, dict)
        assert isinstance(body["id"], int)
        assert isinstance(body["name"], str)
        assert isinstance(body["email"], str)
        assert isinstance(body["auth0_id"], str)


def test_get_user_not_found():
    response = client.get(f"{BASE_ROUTE}/54")
    assert response.status_code == 404
