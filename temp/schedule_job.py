import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class ScheduleJob(Base):
    __tablename__ = "ScheduleJob"
    job_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    trigger_time = Column(DateTime(timezone=True), nullable=False, default=func.now())