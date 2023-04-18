import httpx
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app  # Flask instance of the API

# from oauth2client import GOOGLE_TOKEN_URI, client


test_client = TestClient(app)
client = httpx.AsyncClient()


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


@pytest.fixture(scope="module")
def get_token_id():
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    refresh_token = "1//04puCTtWhEyMiCgYIARAAGAQSNwF-L9IrfZCxCMa5klAX2MxipBNzCbCr2rEgddoS7ejTrWJL9Oza8TJnBcoZPXg6EQgYK3Nwh4w"
    post_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = httpx.post("https://oauth2.googleapis.com/token", json=post_body)

    id_token = response.json()["id_token"]

    return id_token


# test
def test_google_auth(get_server_api, get_token_id):
    credential = get_token_id
    data = {"credential": credential}
    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/auth/sso-login", json=data
    )
    test_client.get(f"{get_server_api}{settings.API_V1_STR}/users/logout")
    assert response.status_code == 200
