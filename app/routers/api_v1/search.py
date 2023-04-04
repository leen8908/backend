from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.post("/matching-room/list", response_model={})  # List[schemas.MatchingRoom])
def search_matching_rooms(
    db: Session = Depends(deps.get_db),
    user_email: str = "",
    prompt: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve matching rooms.
    """
    print('prompt in serach_matching_rooms >>> ', prompt)
    matching_rooms = crud.matching_room.search_with_user_and_name(
        db=db, user_email=user_email, name=prompt)
    return {'message': 'success', 'data': matching_rooms}


@router.post("/group/list", response_model={})  # List[schemas.MatchingRoom])
def search_groups(
    db: Session = Depends(deps.get_db),
    user_email: str = "",
    prompt: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve groups.
    """
    groups = crud.group.search_with_user_and_name(
        db=db, user_email=user_email, name=prompt)
    return {'message': 'success', 'data': groups}
