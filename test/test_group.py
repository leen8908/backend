import json
import unittest
import uuid
from base64 import b64encode
from datetime import datetime
from unittest import mock

from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from app import schemas
from app.core.config import settings
from app.main import app  # Flask instance of the API

client = TestClient(app)

# fake data for test
fake_group = schemas.Group(
    name="test_group_name",
    group_id="test_group_id",
    room_uuid=uuid.uuid4(),
    create_time=datetime.now(),
)
fake_member = schemas.User(
    email="test-email@gmail.com",
    is_admin=True,
    name="test_name",
    line_id="test_line_id",
    image="",
)


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")


class TestGroupAPI(unittest.TestCase):
    @mock.patch("app.routers.api_v1.group.crud.group.search_with_user_and_name")
    def test_read_my_groups_who_has_logged_in(self, mock_my_groups):
        mock_my_groups.return_value = [fake_group]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.get(
            f"{settings.API_V1_STR}/group/my-list",
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.json()["data"][0]["group_id"] == fake_group.group_id

    def test_read_my_groups_who_has_not_logged_in(self):
        response = client.get(f"{settings.API_V1_STR}/group/my-list")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."

    @mock.patch("app.routers.api_v1.search.crud.group.search_with_user_and_name")
    def test_search_groups_who_has_logged_in(self, mock_groups):
        mock_groups.return_value = [fake_group]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.post(
            f"{settings.API_V1_STR}/search/group/list",
            json={"prompt": "test"},
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.json()["data"][0]["group_id"] == fake_group.group_id

    def test_search_groups_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/group/list", json={"prompt": "test"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."
