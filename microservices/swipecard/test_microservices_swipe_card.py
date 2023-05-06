# import datetime
# import os
# import random
# import string
# import sys
# import loguru
# import pytest
# from sqlalchemy import create_engine
# from fastapi.encoders import jsonable_encoder
# from fastapi.testclient import TestClient
# from sqlalchemy.orm import scoped_session,sessionmaker
# from sqlalchemy_utils.functions import create_database, database_exists

# # SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # noqa E402
# # sys.path.append(os.path.dirname(SCRIPT_DIR))
# from microservices.swipecard.core.config import settings
# from microservices.swipecard.swipe import app  # Flask instance of the API
# from microservices.swipecard.swipe import get_db

# from . import crud, schemas
# from .database import Base
# from .models.mr_liked_hated_member import MR_Liked_Hated_Member
# from .models.mr_member import MR_Member
# from .models.user import User
# from .models.matching_room import MatchingRoom

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@\
# {settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/test{settings.POSTGRES_DB}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# if not database_exists(SQLALCHEMY_DATABASE_URL):
#     create_database(SQLALCHEMY_DATABASE_URL)

# # Set up the database once
# # Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="module")
# def db_conn():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()


# @pytest.fixture(scope="module")
# def client():
#     def override_get_db():
#         session = SessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as client:
#         yield client
#     # reset overrides
#     app.dependency_overrides = {}


# # session = scoped_session(
# #     sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # )

# # # Fake data
# # # user
# # for i in range(4):
# #     email="test_admin" + str(i + 1) + "@sdm-teamatch.com"
# #     name="test_admin" + str(i + 1)
# #     is_google_sso=True
# #     db_obj = User(
# #             email=email,
# #             password=None,
# #             name=name,
# #             image=None,
# #             is_admin=False,
# #             is_google_sso=is_google_sso,
# #         )
# #     session.add(db_obj)
# #     session.commit()


# # # matching room
# # db_obj = MatchingRoom(
# #     name="swipe_test_matching_room",
# #     room_id="swipe_test_matching_room001",
# #     due_time=datetime.datetime.now(),
# #     min_member_num=3,
# #     description="",
# #     is_forced_matching=True,
# #     created_time=datetime.datetime.now()
# # )
# # session.add(db_obj)
# # session.commit()

# # # MR_member
# # user_uuids = []
# # for i in range(4):
# #     user =jsonable_encoder(session.query(User).filter(User.email == "test_admin" + str(i + 1) + "@sdm-teamatch.com").first())
# #     user_uuids.append(user["user_uuid"])
# # matching_room = session.query(MatchingRoom).filter(MatchingRoom.room_id == "swipe_test_matching_room001").first()
# # room_uuid = jsonable_encoder(matching_room)["room_uuid"]
# # for uuid in user_uuids:
# #     mr_member_in1 = MR_Member(
# #         user_uuid=uuid,
# #         room_uuid=room_uuid,
# #     )
# #     session.add(mr_member_in1)
# #     session.commit()


# # def delete_fake_data():
#     # delete MR_Liked_Hated_Member
#     # obj = (
#     #     session.query(MR_Liked_Hated_Member)
#     #     .filter(MR_Liked_Hated_Member.room_uuid == room_uuid)
#     #     .first()
#     # )
#     # session.delete(obj)
#     # session.commit()
#     # session.refresh()
#     # # delete mr member
#     # for user_uuid in user_uuids:
#     #     obj = (
#     #         session.query(MR_Member)
#     #         .filter(MR_Member.user_uuid == user_uuid)
#     #         .first()
#     #     )
#     #     session.delete(obj)
#     #     session.commit()
#     #     session.refresh()
#     # # delete matching room
#     # obj = (
#     #     session.query(MatchingRoom)
#     #     .filter(MatchingRoom.room_id == "swipe_test_matching_room001")
#     #     .first()
#     # )
#     # session.delete(obj)
#     # session.commit()
#     # session.refresh()
#     # # delete user
#     # for user_uuid in user_uuids:
#     #     obj = session.query(User).filter(User.user_uuid == user_uuid).first()
#     #     session.delete(obj)
#     #     session.commit()
#     #     session.refresh()
#     # db_obj = User(
#     #         email="ifexistthenright",
#     #         password=None,
#     #         name="ifexistthenright",
#     #         image=None,
#     #         is_admin=False,
#     #         is_google_sso=True,
#     #     )
#     # session.add(db_obj)
#     # session.commit()


# @pytest.fixture(scope="module")
# def get_server_api():
#     server_name = "http://localhost:8002"
#     return server_name


# # Test
# def test_microservice_save_preference(get_server_api, db_conn, client):
#     # Fake data
#     # user
#     for i in range(4):
#         email="swipe_test_admin" + str(i + 1) + "@sdm-teamatch.com"
#         name="test_admin" + str(i + 1)
#         is_google_sso=True
#         db_obj = User(
#                 email=email,
#                 password=None,
#                 name=name,
#                 image=None,
#                 is_admin=False,
#                 is_google_sso=is_google_sso,
#             )
#         db_conn.add(db_obj)
#         try:
#             db_conn.commit()
#         except:
#             db_conn.rollback()
#             raise
#         finally:
#             db_conn.close()


#     # matching room
#     db_obj = MatchingRoom(
#         name="swipetest_matching_room",
#         room_id="swipetest_matching_room001",
#         due_time=datetime.datetime.now(),
#         min_member_num=3,
#         description="",
#         is_forced_matching=True,
#         created_time=datetime.datetime.now()
#     )
#     db_conn.add(db_obj)
#     try:
#         db_conn.commit()
#     except:
#         db_conn.rollback()
#         raise
#     finally:
#         db_conn.close()

#     # MR_member
#     user_uuids = []
#     for i in range(4):
#         user =jsonable_encoder(db_conn.query(User).filter(User.email == "test_admin" + str(i + 1) + "@sdm-teamatch.com").first())
#         user_uuids.append(user["user_uuid"])
#     matching_room = db_conn.query(MatchingRoom).filter(MatchingRoom.room_id == "swipetest_matching_room001").first()
#     room_uuid = jsonable_encoder(matching_room)["room_uuid"]
#     for uuid in user_uuids:
#         mr_member_in1 = MR_Member(
#             user_uuid=uuid,
#             room_uuid=room_uuid,
#         )
#         db_conn.add(mr_member_in1)
#         try:
#             db_conn.commit()
#         except:
#             db_conn.rollback()
#             raise
#         finally:
#             db_conn.close()

#     member = []
#     for i in range(2):
#         member.append(
#             jsonable_encoder(
#                 db_conn.query(MR_Member)
#                 .filter(MR_Member.user_uuid == user_uuids[i])
#                 .first()
#             )
#         )

#     preference = {
#         "member_id": member[0]["member_id"],
#         "room_uuid": room_uuid,
#         "target_member_id": member[1]["member_id"],
#         "is_like": True,
#         "is_hated": False,
#     }

#     response = client.post(
#         f"{get_server_api}/swipe-card/swipe",
#         json=preference,
#     )

#     assert response.status_code == 200
#     assert response.json()["message"] == "success"


# def test_microservice_get_recommendation(get_server_api, db_conn, client):
#     member = jsonable_encoder(db_conn.query(MR_Member).first())
#     matching_room = db_conn.query(MatchingRoom).filter(MatchingRoom.room_id == "swipetest_matching_room001").first()
#     room_uuid = jsonable_encoder(matching_room)["room_uuid"]
#     recommend_in = {"member_id": member["member_id"], "room_uuid": room_uuid}

#     response = client.post(
#         f"{get_server_api}/swipe-card/swipe-recommend",
#         json=recommend_in,
#     )
#     response_data = response.json()["data"]
#     rcmd_member_list = []
#     for d in response_data:
#         rcmd_member_list.append(d["recommended_member_id"])

#     # delete fake data
#     #delete_fake_data()
#     user_uuids = []
#     for i in range(4):
#         user =jsonable_encoder(db_conn.query(User).filter(User.email == "swipe_test_admin" + str(i + 1) + "@sdm-teamatch.com").first())
#         user_uuids.append(user["user_uuid"])
#     obj = (
#         db_conn.query(MR_Liked_Hated_Member)
#         .filter(MR_Liked_Hated_Member.room_uuid == room_uuid)
#         .first()
#     )
#     db_conn.delete(obj)
#     try:
#         db_conn.commit()
#     except:
#         db_conn.rollback()
#         raise
#     finally:
#         db_conn.close()
#     db_conn.refresh()
#     # delete mr member
#     for user_uuid in user_uuids:
#         obj = (
#             db_conn.query(MR_Member)
#             .filter(MR_Member.user_uuid == user_uuid)
#             .first()
#         )
#         db_conn.delete(obj)
#         try:
#             db_conn.commit()
#         except:
#             db_conn.rollback()
#             raise
#         finally:
#             db_conn.close()
#         db_conn.refresh()
#     # delete matching room
#     obj = (
#         db_conn.query(MatchingRoom)
#         .filter(MatchingRoom.room_id == "swipetest_matching_room001")
#         .first()
#     )
#     db_conn.delete(obj)
#     try:
#         db_conn.commit()
#     except:
#         db_conn.rollback()
#         raise
#     finally:
#         db_conn.close()
#     db_conn.refresh()
#     # delete user
#     for user_uuid in user_uuids:
#         obj = db_conn.query(User).filter(User.user_uuid == user_uuid).first()
#         db_conn.delete(obj)
#         db_conn.commit()
#         db_conn.refresh()
#     db_obj = User(
#             email="ifexistthenright",
#             password=None,
#             name="ifexistthenright",
#             image=None,
#             is_admin=False,
#             is_google_sso=True,
#         )
#     db_conn.add(db_obj)
#     try:
#         db_conn.commit()
#     except:
#         db_conn.rollback()
#         raise
#     finally:
#         db_conn.close()

#     assert response.status_code == 200
#     assert response.json()["message"] == "success"
#     assert len(rcmd_member_list) == 2
