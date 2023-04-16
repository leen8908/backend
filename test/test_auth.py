import httplib2
import pytest
from fastapi.testclient import TestClient
from oauth2client import GOOGLE_TOKEN_URI, client

from app.core.config import settings
from app.main import app  # Flask instance of the API

test_client = TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


@pytest.fixture(scope="module")
def get_token_id():
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    refresh_token = "1//04B7dCuIB3h2YCgYIARAAGAQSNwF-L9Ir9uCxqACRC6NeXcLaKuyuhkz2S1I-DNwPfzqQLOwfL-UVkOG6kTWk74jZsSoPCGH7Yp4"

    creds = client.OAuth2Credentials(
        access_token=None,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        token_expiry=None,
        token_uri=GOOGLE_TOKEN_URI,
        user_agent="pythonclient",
    )

    creds.refresh(httplib2.Http())
    id_token = creds.id_token_jwt
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
