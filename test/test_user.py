from app.main import app  # Flask instance of the API
from fastapi.testclient import TestClient
from app.core.config import settings
import pytest
import random
import string


client = TestClient(app)

# @pytest.fixture(scope="module")           #new function
# def normal_user_token_headers(client: TestClient, db_session: Session):
#     return  authentication_token_from_email(
#         client=client, email=settings.TEST_USER_EMAIL, db=db_session
#     )
@pytest.fixture(scope="module")
def get_server_api():
    server_name = f"http://localhost:8000"
    return server_name

@pytest.fixture(scope="module")
def get_user_token_headers():
    server_api = get_server_api()
    login_data = {
        "username": "user1",
        "password": "string",
    }
    response = client.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # user_token_headers = headers
    return headers

@pytest.fixture(scope="module")
def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))

def test_read_user_by_existing_email(get_server_api):
    email = "user1@example.com"
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/profile", json={"email": email})
    assert 200 <= response.status_code < 300
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"

def test_read_user_by_not_existing_email(get_server_api):
    email = "wrongmail@example.com"
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/profile", json={"email": email})
    assert response.status_code == 400

def test_update_user_profile(get_server_api):
    update_data = {"email": "user1@example.com","line_id": "123456"}
    response = client.put(f"{get_server_api}{settings.API_V1_STR}/users/profile", json=update_data)
    assert 200 <= response.status_code < 300
    assert update_data["email"] == response.json()["data"]["email"]
    assert response.json()["message"] == "success"

def test_create_new_user(get_server_api, random_lower_string):
    email = random_lower_string+"@example.com"
    name = random_lower_string
    password = random_lower_string
    data = {"email": email, "name": name, "password": password}
    response = client.post(
        f"{get_server_api}{settings.API_V1_STR}/users/",
        json=data
    )
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert email == created_user["email"]

def test_create_existing_user(get_server_api, random_lower_string):
    email = "user1@example.com"
    name = random_lower_string
    password = random_lower_string
    data = {"email": email, "name": name, "password": password}
    response = client.post(
        f"{get_server_api}{settings.API_V1_STR}/users/",
        json=data
    )
    assert response.status_code == 400
    assert response.json()["message"] == "The user with this email already exists in the system."

# def test_user_google_login():
