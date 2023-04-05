import os
from fastapi import APIRouter, Depends, HTTPException, Response, FastAPI, APIRouter, Form
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from starlette.responses import RedirectResponse
from app import crud
from app.routers import deps
from app.routers.api_v1.login import login_access_token
from typing import Any
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from app.schemas.user import UserCreate
from app.routers.api_v1.login import google_login_access_token
import loguru
from datetime import timedelta
from app.core import security
from fastapi.encoders import jsonable_encoder


# Create the auth app
router = APIRouter()


# # OAuth settings
# GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID or None
# GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET or None
# if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
#     raise HTTPException(501, 'Missing env variables')

# # Set up oauth
# config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
# starlette_config = Config(environ=config_data)
# oauth = OAuth(starlette_config)
# oauth.register(
#     name='google',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile'},
# )

@router.post('/sso-login')
def google_auth(request:Request, response: Response, db: Session =Depends(deps.get_db), credential: str = Form(...)) -> Any:
    """
    Google credential decode
    """
    # Supplied by g_id_onload
    tokenid = credential
    try:
        idinfo = id_token.verify_oauth2_token(tokenid, requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=5)
        
        # # 檢查此google帳號是否已建立帳號
        user = crud.user.get_by_email(db, email=idinfo['email'])

         #帳號尚未建立，create user
        if not user:
            user_in = UserCreate(**{
                "email": idinfo["email"],
                "name": idinfo["name"],
                "image": idinfo["picture"],
                "is_google_sso": True
                }
            )
            crud.user.create(db, obj_in=user_in)
        
        #帳號已建立，取得access token
        user = crud.user.get_by_email(db, email=idinfo['email'])
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.user_uuid, expires_delta=access_token_expires
        )
        request.session['user'] = jsonable_encoder(user)
        request.session['authorization'] = access_token
        response.set_cookie(
            "access_token",
            access_token,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            True,
            "lax",
        )

        response.set_cookie(
            "logged_in",
            "True",
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            False,
            "lax",
        )
        access_token= {
                "access_token": access_token,
                "token_type": "bearer",
        }

        # 回傳 Matching room list

        return 
    except ValueError:
        # Invalid token
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized", "data": None},
        )
    # data = parseJwt(response.credential)
    # request.session['user'] = dict(user_data)
    # # 檢查此google帳號是否已建立帳號
    # user = crud.user.get_by_email(Depends(deps.get_db), email=dict(user_data).email)

    # #帳號已建立，回傳 matchingRoom
    # if user:
    #     return
    # #帳號尚未建立，create user
    # else:

# GOOGLE_SECRET_KEY = settings.GOOGLE_SECRET_KEY or None
# if GOOGLE_SECRET_KEY is None:
#     raise 'Missing SECRET_KEY'
# auth_app.add_middleware(SessionMiddleware, secret_key=GOOGLE_SECRET_KEY)

# @auth_app.post('/sso-login')
# async def login(request: Request):
#     redirect_uri = request.url_for('auth-token')  # This creates the url for the /google-auth endpoint
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @auth_app.post('/auth-token')
# async def auth(request: Request):
#     try:
#         access_token = await oauth.google.authorize_access_token(request)
#     except OAuthError:
#         return HTTPException(
#             status_code=401,
#             detail='Could not validate credentials',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     user_data = await oauth.google.parse_id_token(request, access_token)
#     request.session['user'] = dict(user_data)
#     # 檢查此google帳號是否已建立帳號
#     user = crud.user.get_by_email(Depends(deps.get_db), email=dict(user_data).email)

#     #帳號已建立，回傳 matchingRoom
#     if user:
#         return
#     #帳號尚未建立，create user
#     else:
