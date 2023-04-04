import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class MR_Member(Base):
    __tablename__ = "MR_Member"
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid"), primary_key=True, nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), primary_key=True, nullable=False
    )
    join_time = Column(DateTime(timezone=True), default=func.now())
    leave_time = Column(DateTime(timezone=True))
    is_left = Column(Boolean, nullable=False, default=False)
    is_bound = Column(Boolean, nullable=False, default=False)
    liked_user_list = Column(ARRAY(UUID(as_uuid=True)), ForeignKey("User.user_uuid"))
    hated_user_list = Column(ARRAY(UUID(as_uuid=True)), ForeignKey("User.user_uuid"))
    self_tag_list = Column(ARRAY(String), ForeignKey("Tag.tag_text"))
    find_tag_list = Column(ARRAY(String), ForeignKey("Tag.tag_text"))
    rcm_list = Column(
        ARRAY(UUID(as_uuid=True)), ForeignKey("User.user_uuid")
    )
    bind_uuid = Column(
        UUID(as_uuid=True), ForeignKey("BindUser.bind_uuid")
    )