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
fake_notification = schemas.NotificationViewModel(
    receiver_uuid=uuid.uuid4(), send_time=datetime.now(), content=""
)


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")


class TestNotificationAPI(unittest.TestCase):
    @mock.patch(
        "app.routers.api_v1.notification.crud.notification.get_by_receiver_uuid"
    )
    def test_read_my_notifications_who_has_logged_in(self, mock_my_notifications):
        mock_my_notifications.return_value = [fake_notification]
        user = {"email": "", "name": "", "user_uuid": ""}
        response = client.get(
            f"{settings.API_V1_STR}/notification/my-list",
            cookies={"session": create_session_cookie({"user": user})},
        )
        client.get(f"{settings.API_V1_STR}/users/logout")
        assert response.status_code == 200
        assert response.json()["data"][0]["receiver_uuid"] == str(
            fake_notification.receiver_uuid
        )

    def test_read_my_notifications_who_has_not_logged_in(self):
        response = client.get(f"{settings.API_V1_STR}/notification/my-list")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials."
