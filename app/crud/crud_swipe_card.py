# import uuid
# from datetime import datetime
# from typing import Optional

# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Session

# from app.crud.base import CRUDBase
# from app.schemas.swipe_card import SwipeCard


# class CRUDSwipeCard(CRUDBase[SwipeCard,]):
#     # TODO: separate each function or one function with dynamic filter?
#     def get_by_room_uuid(
#         self, db: Session, *, room_uuid: UUID
#     ) -> Optional[MatchingRoom]:
#         return (
#             db.query(MatchingRoom).filter(MatchingRoom.room_uuid == room_uuid).first()
#         )

#     def get_by_room_id(self, db: Session, *, room_id: str) -> Optional[MatchingRoom]:
#         return db.query(MatchingRoom).filter(MatchingRoom.room_id == room_id).first()

#     def create(self, db: Session, *, obj_in: MatchingRoomCreate) -> MatchingRoom:
#         db_obj = MatchingRoom(
#             room_uuid=uuid.uuid4(),  # generate a uuid as room_uuid
#             name=obj_in.name,
#             room_id=obj_in.room_id,
#             due_time=obj_in.due_time,
#             min_member_num=obj_in.min_member_num,
#             description=obj_in.description,
#             is_forced_matching=obj_in.is_forced_matching,
#             created_time=datetime.now(),
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def delete(self, db: Session, *, db_obj: MatchingRoom, room_id: str):
#         if room_id is not None or room_id != "":
#             db_obj = self.get_by_room_id(room_id)
#             db.delete(db_obj)
#             db.commit()
#         return True


# matching_room = CRUDSwipeCard(SwipeCard)
