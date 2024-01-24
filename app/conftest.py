import http.client
import json
import os

import pytest
from dotenv import load_dotenv


def get_token() -> str:
    load_dotenv()

    conn = http.client.HTTPSConnection("thegrapefruitsduo.us.auth0.com")

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    audience = os.getenv("AUTH0_API_AUDIENCE")

    if None in [client_id, client_secret, audience]:
        raise ValueError("Missing environment variables")

    payload_dict = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
        "grant_type": "client_credentials",
    }

    payload = json.dumps(payload_dict)

    headers = {"content-type": "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()
    body = json.loads(data.decode("utf-8"))
    token = body["access_token"]
    if not token:
        raise Exception("error retrieving token")
    return token


@pytest.fixture(scope="session", autouse=True)
def jwt_token():
    token = get_token()
    return token


if __name__ == "__main__":
    token = get_token()
