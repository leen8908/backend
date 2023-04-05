"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class NotificationBase(BaseModel):
    notification_uuid: UUID

# Properties to receive via API on creation


class NotificationCreate(NotificationBase):
    receiver_uuid: UUID
    sender_uuid: UUID
    send_time: datetime
    template_uuid: UUID
    f_string: str

# Properties to receive via API on update


class NotificationUpdate(NotificationBase):
    pass


class NotificationInDBBase(NotificationBase):
    receiver_uuid: UUID
    sender_uuid: UUID
    send_time: datetime
    template_uuid: UUID
    f_string: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Notification(NotificationInDBBase):
    pass


# Additional properties stored in DB
class NotificationInDB(NotificationInDBBase):
    pass


class NotificationTextWithMessage(BaseModel):
    message: str
    data: Optional[List[str]] = None
