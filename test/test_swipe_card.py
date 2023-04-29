import json
import random
import string
from base64 import b64encode
from datetime import timedelta

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from app import crud
from app.core import security
from app.core.config import settings
from app.database.session import db_session
from app.main import app  # Flask instance of the API

client = TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_user_authentication_headers():
    email = "admin@sdm-teamatch.com"

    user = crud.user.get_by_email(db=db_session, email=email)
    user = jsonable_encoder(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user["user_uuid"], expires_delta=access_token_expires
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


# Test
# def test_save_preference_who_has_logged_in(get_server_api):
#     preference = {
#         "member_id": "1",
#         "room_uuid": "6891704b-a2e8-4fce-b971-b3fe3928dfd6",
#         "target_member_id": "4",
#         "is_like": True,
#         "is_hated": False
#     }

#     response = client.post(
#         f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe",
#         headers=get_user_authentication_headers(),
#         json=preference
#     )

#     assert response.status_code == 200
#     assert response.json()["message"] == "success"


