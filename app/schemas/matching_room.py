"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class MatchingRoomBase(BaseModel):
    room_uuid: UUID

# Properties to receive via API on creation


class MatchingRoomCreate(MatchingRoomBase):
    name: Optional[str] = None
    room_id: str
    due_time: datetime
    min_member_num: int
    description: Optional[str] = None
    is_forced_matching: bool = False
    created_time: datetime  # .now()

# Properties to receive via API on update


class MatchingRoomUpdate(MatchingRoomBase):
    pass


class MatchingRoomInDBBase(MatchingRoomBase):
    name: Optional[str]
    room_id: str
    due_time: datetime
    min_member_num: int
    description: Optional[str] = None
    is_forced_matching: bool = False
    created_time: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class MatchingRoom(MatchingRoomInDBBase):
    pass


# Additional properties stored in DB
class MatchingRoomInDB(MatchingRoomInDBBase):
    is_closed: bool = False
    finish_time: datetime
