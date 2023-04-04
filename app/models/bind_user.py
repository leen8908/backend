import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class BindUser(Base):
    __tablename__ = "BindUser"
    bind_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    bind_time = Column(DateTime(timezone=True), default=func.now())
    room_uuid = Column(UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False)