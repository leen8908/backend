from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.post("/my-list", response_model={})  # List[schemas.MatchingRoom])
def read_my_matching_rooms(
    db: Session = Depends(deps.get_db),
    user_email: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve user's matching rooms.
    """
    matching_rooms = crud.matching_room.search_with_user_and_name(
        db=db, user_email=user_email)
    return {'message': 'success', 'data': matching_rooms}


# @router.post("/", response_model=schemas.MatchingRoom)
# def create_matching_room(
#     *,
#     db: Session = Depends(deps.get_db),
#     matching_room_in: schemas.MatchingRoomCreate,
#     current_user: models.user = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Create new matching room.
#     """
#     matching_room = crud.matching_room.get_by_room_id(
#         db, room_id=matching_room_in.room_id)
#     if matching_room:
#         raise HTTPException(
#             status_code=400,
#             detail="The matching room with this room_id already exists in the system.",
#         )
#     matching_room = crud.matching_room.create(db, obj_in=matching_room_in)
#     return matching_room


# @router.delete("/", response_model=dict)
# def delete_matching_room(
#     db: Session = Depends(deps.get_db),
#     room_id: str = "",
#     current_user: models.user = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete matching room with room_id.
#     """
#     matching_room = crud.matching_room.get_by_room_id(
#         db, room_id=room_id)
#     if not matching_room:
#         raise HTTPException(
#             status_code=400,
#             detail="No matching room to delete.",
#         )
#     isDeleteSuccessfully = crud.matching_room.delete(db, room_id)
#     if isDeleteSuccessfully:
#         return {"message": "Success"}
#     else:
#         return {"message": "Fail"}
