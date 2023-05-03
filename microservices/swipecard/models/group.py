import os
import sys
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# from app.database.base_class import Base
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from swipecard.database import Base


class Group(Base):
    __tablename__ = "Group"
    group_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
    create_time = Column(DateTime(timezone=True), default=func.now())
    group_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
