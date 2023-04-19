import json
import unittest
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
fake_matching_room = schemas.MatchingRoom(
    room_id="test_room_id", due_time=datetime.now(), min_member_num=3
)
fake_matching_room.name = "test_matching_room"
fake_matching_room.description = "test_desc"
fake_matching_room.is_forced_matching = True
fake_matching_room.created_time = None
# fake_matching_room.room_id = "test_room_id"
# fake_matching_room.min_member_num = 3
# fake_matching_room.due_time = datetime.now()


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")


class TestMatchingRoomAPI(unittest.TestCase):
    @mock.patch(
        "app.routers.api_v1.matching_room.crud.matching_room.search_with_user_and_name"
    )
    def test_read_my_matching_rooms_who_has_logged_in(self, mock_my_matching_rooms):
        mock_my_matching_rooms.return_value = [fake_matching_room]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.get(
            f"{settings.API_V1_STR}/matching-room/my-list",
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_read_my_matching_rooms_who_has_not_logged_in(self):
        response = client.get(f"{settings.API_V1_STR}/matching-room/my-list")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."

    @mock.patch(
        "app.routers.api_v1.search.crud.matching_room.search_with_user_and_name"
    )
    def test_search_matching_rooms_who_has_logged_in(self, mock_matching_rooms):
        mock_matching_rooms.return_value = [fake_matching_room]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": True},
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_search_matching_rooms_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": True},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."

    @mock.patch(
        "app.routers.api_v1.search.crud.matching_room.search_with_user_and_name"
    )
    def test_search_matching_rooms_with_user_who_has_logged_in(
        self, mock_matching_rooms
    ):
        mock_matching_rooms.return_value = [fake_matching_room]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": False},
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_search_matching_rooms_with_user_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": False},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."

    def test_search_matching_rooms_missing_param_who_has_logged_in(self):
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM"},
            cookies={"session": create_session_cookie({"user": user})},
        )
        assert response.status_code == 422

    def test_search_matching_rooms_missing_param_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": ""},
        )
        assert response.status_code == 422
