# from app.database.base_class import Base
import os
import sys
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from swipecard.database import Base


class NotificationTemplate(Base):
    __tablename__ = "NotificationTemplate"
    template_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    text = Column(String, nullable=False)
