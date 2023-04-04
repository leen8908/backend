"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class GroupBase(BaseModel):
    group_uuid: UUID

# Properties to receive via API on creation


class GroupCreate(GroupBase):
    name: str
    group_id: str
    room_uuid: UUID
    created_time: datetime  # .now()

# Properties to receive via API on update


class GroupUpdate(GroupBase):
    pass


class GroupInDBBase(GroupBase):
    name: str
    group_id: str
    room_uuid: UUID
    created_time: datetime  # .now()

    class Config:
        orm_mode = True


# Additional properties to return via API
class Group(GroupInDBBase):
    pass


# Additional properties stored in DB
class GroupInDB(GroupInDBBase):
    pass
