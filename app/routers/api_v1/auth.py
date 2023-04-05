# import os
# from fastapi import APIRouter, Depends, HTTPException, Response, FastAPI
# from authlib.integrations.starlette_client import OAuth
# from authlib.integrations.starlette_client import OAuthError
# from fastapi import FastAPI
# from fastapi import Request
# from starlette.config import Config
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.responses import JSONResponse
# from app.core.config import settings
# from starlette.responses import RedirectResponse
# from app import crud
# from app.routers import deps
# from app.routers.api_v1.login import login_access_token
# from typing import Any

# # Create the auth app
# auth_app = FastAPI()


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

# @auth_app.post('/sso-login')
# def google_auth(credential: dict) -> Any:
    # """
    # Google credential decode
    # """
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
