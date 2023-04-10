"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""

from typing import Optional, List

from pydantic import BaseModel
from . import User
from . import MatchingRoom


# Shared properties
class SSOLoginBase(BaseModel):
    access_token: Optional[str] = None

class SSOLogin(SSOLoginBase):
    user: Optional[User] = None
    matching_rooms: Optional[List[MatchingRoom]] = None

class SSOLoginMessage(BaseModel):
    message:str
    data: Optional[SSOLogin] = None