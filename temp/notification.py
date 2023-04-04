import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Notification(Base):
    __tablename__ = "Notification"
    notification_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    receiver_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid"), nullable=False
    )
    sender_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid")
    )
    send_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    template_uuid = Column(String, nullable=False)
    f_string = Column(String)