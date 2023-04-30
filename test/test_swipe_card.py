import datetime
import random
import string
from datetime import timedelta

import pytest
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.database.base_class import Base
from app.main import app  # Flask instance of the API
from app.models.mr_liked_hated_member import MR_Liked_Hated_Member
from app.models.mr_member import MR_Member
from app.routers.deps import get_db

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@\
{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/test.db"

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# This fixture creates a nested transaction,
# recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override, it uses the one provided by the session fixture.
@pytest.fixture()
def test_client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_user_authentication_headers(session, email):
    email = email

    user = crud.user.get_by_email(db=session, email=email)
    user = jsonable_encoder(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user["user_uuid"], expires_delta=access_token_expires
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


# Test
def test_save_preference_who_has_logged_in(get_server_api, session, test_client):
    # generate fake data
    email1 = "test_admin1@sdm-teamatch.com"
    email2 = "test_admin2@sdm-teamatch.com"
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email1, name="test_admin1", is_google_sso=True),
    )
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email2, name="test_admin2", is_google_sso=True),
    )
    user1 = crud.user.get_by_email(session, email=email1)
    user2 = crud.user.get_by_email(session, email=email2)
    user_uuid1 = user1.user_uuid
    user_uuid2 = user2.user_uuid

    matching_room_in = schemas.MatchingRoomCreate(
        name="test_matching_room",
        room_id="test_matching_room001",
        due_time=datetime.datetime.now(),
        min_member_num=3,
    )
    crud.matching_room.create(session, obj_in=matching_room_in)
    matching_room = crud.matching_room.get_by_room_id(
        session, room_id="test_matching_room001"
    )
    room_uuid = jsonable_encoder(matching_room)["room_uuid"]

    mr_member_in1 = MR_Member(
        user_uuid=user_uuid1,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in1)
    session.commit()
    mr_member_in2 = MR_Member(
        user_uuid=user_uuid2,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in2)
    session.commit()

    preference = {
        "member_id": "1",
        "room_uuid": room_uuid,
        "target_member_id": "2",
        "is_like": True,
        "is_hated": False,
    }

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe",
        headers=get_user_authentication_headers(session=session, email=email1),
        json=preference,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"


def test_save_preference_who_has_not_logged_in(get_server_api, test_client):
    preference = {
        "member_id": "1",
        "room_uuid": "6891704b-a2e8-4fce-b971-b3fe3928dfd6",
        "target_member_id": "2",
        "is_like": True,
        "is_hated": False,
    }

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe", json=preference
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_recommendation(get_server_api, session, test_client):
    # generate fake data
    email1 = "test_admin1@sdm-teamatch.com"
    email2 = "test_admin2@sdm-teamatch.com"
    email3 = "test_admin3@sdm-teamatch.com"
    email4 = "test_admin4@sdm-teamatch.com"
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email1, name="test_admin1", is_google_sso=True),
    )
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email2, name="test_admin2", is_google_sso=True),
    )
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email3, name="test_admin3", is_google_sso=True),
    )
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(email=email4, name="test_admin4", is_google_sso=True),
    )
    user1 = crud.user.get_by_email(session, email=email1)
    user2 = crud.user.get_by_email(session, email=email2)
    user3 = crud.user.get_by_email(session, email=email3)
    user4 = crud.user.get_by_email(session, email=email4)
    user_uuid1 = user1.user_uuid
    user_uuid2 = user2.user_uuid
    user_uuid3 = user3.user_uuid
    user_uuid4 = user4.user_uuid

    matching_room_in = schemas.MatchingRoomCreate(
        name="test_matching_room",
        room_id="test_matching_room001",
        due_time=datetime.datetime.now(),
        min_member_num=3,
    )
    crud.matching_room.create(session, obj_in=matching_room_in)
    matching_room = crud.matching_room.get_by_room_id(
        session, room_id="test_matching_room001"
    )
    room_uuid = jsonable_encoder(matching_room)["room_uuid"]

    mr_member_in1 = MR_Member(
        member_id=1,
        user_uuid=user_uuid1,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in1)
    session.commit()
    mr_member_in2 = MR_Member(
        member_id=2,
        user_uuid=user_uuid2,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in2)
    session.commit()
    mr_member_in3 = MR_Member(
        member_id=3,
        user_uuid=user_uuid3,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in3)
    session.commit()
    mr_member_in4 = MR_Member(
        member_id=4,
        user_uuid=user_uuid4,
        room_uuid=room_uuid,
    )
    session.add(mr_member_in4)
    session.commit()

    preference_in = MR_Liked_Hated_Member(
        member_id=1,
        room_uuid=room_uuid,
        target_member_id=3,
        is_liked=True,
        is_hated=False,
    )
    session.add(preference_in)
    session.commit()

    recommend_in = {"member_id": "1", "room_uuid": room_uuid}

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe-recommend",
        headers=get_user_authentication_headers(session=session, email=email1),
        json=recommend_in,
    )
    response_data = response.json()["data"]
    rcmd_member_list = []
    for d in response_data:
        rcmd_member_list.append(d["recommended_member_id"])

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert len(rcmd_member_list) == 2
