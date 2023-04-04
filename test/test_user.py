from app.main import app  # Flask instance of the API
from fastapi.testclient import TestClient

client = TestClient(app)


# def test_get_user_profile():
#     response = client.get("/api/v1/users")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}

# def test_update_user_profile():

# def test_create_user():

# def test_user_google_login():
