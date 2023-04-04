from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    #current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/profile/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current logged-in user's profile.
    """
    return current_user


@router.post("/profile", response_model=schemas.User)
def read_user_by_email(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserGetBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Read active user's profile by email for super user only.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    return user
    


@router.put("/profile", response_model=schemas.User)
def update_user_profile(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserInDBBase,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current logged-in user's profile.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    
    
    return user