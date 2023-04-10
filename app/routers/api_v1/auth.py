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
from app import crud, schemas
from app.routers import deps
from app.routers.api_v1.login import login_access_token
from typing import Any
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from app.schemas.user import UserCreate, UserCredential
import loguru
from datetime import timedelta
from app.core import security
from fastapi.encoders import jsonable_encoder


# Create the auth app
router = APIRouter()


@router.post('/sso-login',response_model=schemas.SSOLoginMessage)
#def google_auth(request:Request, response: Response, db: Session =Depends(deps.get_db), credential:str= Form(...)) -> Any: # for google 重新導向URI(google重新導向怪怪的應該不會用這個ㄌ)
def google_auth(request:Request, response: Response, db: Session =Depends(deps.get_db), credential: UserCredential = None) -> Any: # for 前端直接傳 credential
    """
    Google credential decode and authentication
    """
    # Supplied by g_id_onload
    tokenid = credential.credential
    #tokenid = credential
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

        
        matching_rooms = crud.matching_room.search_with_user_and_name(db)

        # 回傳 token, user, Matching room list
        return {'message': 'success', 'data': {"access_token": access_token["access_token"], "user": user, "matching_rooms":matching_rooms}}
    
    except ValueError:
        # Invalid token
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )