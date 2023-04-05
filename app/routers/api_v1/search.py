from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.post("/matching-room/list", response_model=schemas.MatchingRoomWithMessage)
def search_matching_rooms(
    db: Session = Depends(deps.get_db),
    user_email: str = "",
    prompt: str = "",
    query_all: bool = True  # ,
    # current_user: models.user = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve matching rooms.
    """
    if (query_all):
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db, name=prompt)
    else:  # query with user authentication
        #  先看user_email是否找得到user再去query matching room
        if (user_email == ''):
            raise HTTPException(
                status_code=400,
                detail="Fail to retrieve user's matching room. Missing parameter: user_email."
            )
        user = crud.user.get_by_email(db=db, email=user_email)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Fail to find user with this email.",
            )
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db, user_uuid=user.user_uuid, name=prompt)
    return {'message': 'success', 'data': matching_rooms}


@router.post("/group/list", response_model=schemas.GroupWithMessage)
def search_my_groups(
    db: Session = Depends(deps.get_db),
    user_email: str = "",
    prompt: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve groups.
    """
    #  先看user_email是否找得到user再去query group
    if (user_email == ''):
        raise HTTPException(
            status_code=400,
            detail="Fail to retrieve user's group. Missing parameter: user_email."
        )
    user = crud.user.get_by_email(db=db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Fail to find user with this email.",
        )
    groups = crud.group.search_with_user_and_name(
        db=db, user_uuid=user.user_uuid, name=prompt)
    return {'message': 'success', 'data': groups}
