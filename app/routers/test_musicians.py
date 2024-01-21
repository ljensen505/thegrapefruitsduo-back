import requests
from fastapi.testclient import TestClient

from app import app

client = TestClient(app=app)
MUSICIAN_ATTRS = ["id", "name", "bio", "headshot_id"]
BASE_ROUTE = "/musicians"


def test_musician_route_exists():
    response = client.get(BASE_ROUTE)
    assert response.status_code == 200


def test_musician_route_details():
    response = client.get(BASE_ROUTE)
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2

    for musician in body:
        assert all(attr in musician for attr in MUSICIAN_ATTRS)


def test_get_musician():
    response = client.get(f"{BASE_ROUTE}/1")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["bio"], str)
    assert isinstance(body["headshot_id"], str)


def test_get_musician_not_found():
    response = client.get("/musicians/3")
    assert response.status_code == 404


def test_update_headshot():
    orig_url = "https://res.cloudinary.com/dreftv0ue/image/upload/v1705713206/margarite_copy_a4oxty.jpg"
    r = requests.get(orig_url, allow_redirects=True)
    orig_file_object = r.content

    response = client.post(
        "/musicians/1/headshot",
        files={"file": open("app/admin/test_images/IMG_5679.jpg", "rb")},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["bio"], str)
    assert isinstance(body["headshot_id"], str)
    assert body["headshot_id"] != "test_id"

    new_headshot_id = body["headshot_id"]

    response = client.get("/musicians/1")
    body = response.json()
    assert body["headshot_id"] == new_headshot_id

    # reset headshot
    response = client.post(
        "/musicians/1/headshot",
        files={"file": orig_file_object},
    )
