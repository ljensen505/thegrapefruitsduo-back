from fastapi.testclient import TestClient

from app import app, jwt_token
from app.models import Group

client = TestClient(app=app)
GROUP_ATTRS = [attr for attr in Group.model_fields if not attr.startswith("_")]
BASE_ROUTE = "/group"


def test_route_exists():
    response = client.get(BASE_ROUTE)
    assert response.status_code == 200


def test_group_attrs():
    response = client.get(BASE_ROUTE)
    body = response.json()
    assert isinstance(body, dict)
    assert len(body) >= 2

    assert all(attr in body for attr in GROUP_ATTRS)

    assert isinstance(body["name"], str)
    assert isinstance(body["bio"], str)
    assert isinstance(body["id"], int)


def test_cannot_post():
    response = client.post(BASE_ROUTE)
    assert response.status_code == 405


def test_patch_secured():
    response = client.patch(BASE_ROUTE)
    assert response.status_code == 403


def test_patch(jwt_token: str):
    group = client.get(BASE_ROUTE).json()
    old_bio = str(group["bio"])
    new_bio = "clever new bio for the group"
    group["bio"] = new_bio
    response = client.patch(
        BASE_ROUTE, headers={"Authorization": f"Bearer {jwt_token}"}, json=group
    )
    assert response.status_code == 200
    assert response.json()["bio"] == new_bio
    assert response.json()["bio"] != old_bio

    # reset bio
    group["bio"] = old_bio
    client.patch(
        BASE_ROUTE, headers={"Authorization": f"Bearer {jwt_token}"}, json=group
    )
    assert client.get(BASE_ROUTE).json()["bio"] == old_bio
