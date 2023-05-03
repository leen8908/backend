# from app.database.base_class import Base
import os
import sys
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from swipecard.database import Base


class ScheduledJob(Base):
    __tablename__ = "ScheduledJob"
    job_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    trigger_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
