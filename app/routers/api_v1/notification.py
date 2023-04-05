from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.post("/my-list", response_model=schemas.NotificationTextWithMessage)
def read_my_notifications(
    db: Session = Depends(deps.get_db),
    user_email: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve user's notifications.
    """
    #  先看user_email是否找得到user再去query matching room
    if (user_email == ''):
        raise HTTPException(
            status_code=400,
            detail="Fail to retrieve user's notifications. Missing parameter: user_email."
        )
    user = crud.user.get_by_email(db=db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Fail to find user with this email.",
        )
    notifications = crud.notification.get_by_receiver_uuid(
        db=db, receiver_uuid=user.user_uuid)

    return {'message': 'success', 'data': notifications}
