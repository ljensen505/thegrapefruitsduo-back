from fastapi.testclient import TestClient

from app import app, jwt_token
from app.models import Musician

client = TestClient(app=app)
MUSICIAN_ATTRS = [attr for attr in Musician.model_fields if not attr.startswith("_")]
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


def test_update_headshot_secured():
    response = client.post(f"{BASE_ROUTE}/1/headshot")
    assert response.status_code == 403


def test_update_bio_secured():
    response = client.patch(f"{BASE_ROUTE}/1")
    assert response.status_code == 403


# TODO: WRITE FUNC TO GET TOKEN


def test_update_bio(jwt_token: str):
    musician = client.get(f"{BASE_ROUTE}/1").json()
    old_bio = str(musician["bio"])
    new_bio = "clever new bio for the musician"
    musician["bio"] = new_bio
    response = client.patch(
        f"{BASE_ROUTE}/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json=musician,
    )
    assert response.status_code == 200
    assert response.json()["bio"] == new_bio
    assert response.json()["bio"] != old_bio

    # reset bio
    musician["bio"] = old_bio
    client.patch(
        f"{BASE_ROUTE}/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json=musician,
    )
    assert client.get(f"{BASE_ROUTE}/1").json()["bio"] == old_bio


def test_update_headshot(jwt_token: str):
    musician = client.get(f"{BASE_ROUTE}/1").json()
    old_headshot_id = str(musician["headshot_id"])
    headshot_file = "app/admin/test_images/IMG_5679.jpg"
    with open(headshot_file, "rb") as hf:
        file_obj = hf.read()
        response = client.post(
            f"{BASE_ROUTE}/1/headshot",
            headers={"Authorization": f"Bearer {jwt_token}"},
            files={"file": file_obj},
        )
    assert response.status_code == 200
    assert response.json()["headshot_id"] != old_headshot_id

    # reset headshot
    headshot_file = "app/admin/test_images/mg_headshot.jpg"
    with open(headshot_file, "rb") as hf:
        upload_file = hf.read()
        client.post(
            f"{BASE_ROUTE}/1/headshot",
            headers={"Authorization": f"Bearer {jwt_token}"},
            files={"file": upload_file},
        )
