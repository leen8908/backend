from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, ORJSONResponse

from sqlalchemy.orm import Session
from fastapi import Request
from app import crud, models, schemas
from app.routers import deps
from app.core import security
from app.core.config import settings
import loguru
from pydantic import EmailStr

# from google.oauth2 import id_token
# from google.auth.transport import requests


#from fastapi_sso.sso.google import GoogleSSO

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:

    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        loguru.logger.info("Incorrect email or password")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        loguru.logger.info("Inactive user")
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        user.user_uuid, expires_delta=access_token_expires
    )

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
    return {
            "access_token": access_token,
            "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.user = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.post("/google-login/access-token", response_model=schemas.Token)
def google_login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:

    """
    已驗證google登入帳號，直接產生token
    """
    user = crud.user.get_by_email(db, email=form_data.username)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        user.user_uuid, expires_delta=access_token_expires
    )

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
    return {
            "access_token": access_token,
            "token_type": "bearer",
    }

# UNFINISHED: google sso
# @router.post("/sso-login", response_model=schemas.User)
# def google_auth(request: Request,token:str) -> Any:
#     """
#     Google credential decode
#     """
#     try:
#         # Specify the CLIENT_ID of the app that accesses the backend:
#         user =id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

#         request.session['user'] = dict({
#             "email" : user["email"] ,
#             "account_id": user["sub"],
#             "name" : user["name"],
#             "picture": user["picture"]
#         })

#         # 檢查此google帳號是否已建立帳號
#         user = crud.user.get_by_email(Depends(deps.get_db), email=user.email)

#         #帳號尚未建立，create user
#         if not user:
#             user_in = schemas.UserCreate(**{"email": user.email, "name": user.name, "password": user.sub, "image": user.picture})
#             user = crud.user.create(Depends(deps.get_db), obj_in=user_in)

#         #回傳 matchingRoom



#     except ValueError:
#         raise JSONResponse(
#             status_code=400,
#             content={"message": "invalid token", "data": None}
#         )





### ----ignore------
    # data = parseJwt(response.credential)
    # request.session['user'] = dict(user_data)


# google_sso = GoogleSSO(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET)
# @router.get("/google-sso-login")
# # async def google_login(request: Request):
# #     redirect_uri = request.url_for('auth')
# #     return await oauth.google.authorize_redirect(request, redirect_uri)
# async def google_login(request: Request):
#     """Generate login url and redirect"""
#     return await google_sso.get_login_redirect(redirect_uri=request.url_for("google_callback"))


# @router.get("/google/callback")
# async def google_callback(request: Request):
#     """Process login response from Google and return user info"""
#     user = await google_sso.verify_and_process(request)
#     if user is None:
#         raise HTTPException(401, "Failed to fetch user information")
#     return {
#         "id": user.id,
#         "picture": user.picture,
#         "name": user.display_name,
#         "email": user.email,
#         "provider": user.provider,
#     }
