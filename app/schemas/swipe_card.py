"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""

from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class SwipeCardBase(BaseModel):
    member_id: str = None
    room_id: str


class SwipeCardPreference(SwipeCardBase):
    target_member_id: str
    is_liked: bool


class SwipeCardInDBBase(SwipeCardBase):
    tag_text: Optional[str]

    class Config:
        orm_mode = True


class SwipeCard(BaseModel):
    self_tag_text: Optional[str]
    find_tag_text: Optional[str]
    image: Optional[str]
    name: Optional[str]


class SwipeCardInDB(SwipeCardInDBBase):
    is_self_tag: bool
    is_find_tag: bool

    class Config:
        orm_mode = True


# ask for recommendation
class SwipeCardRecommend(SwipeCardBase):
    pass


class SwipeCardMessage(BaseModel):
    message: str
    data: Optional[List[SwipeCard]] = None
