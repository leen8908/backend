from typing import List,Tuple, Any
from abc import ABC, abstractmethod
from app import crud, models, schemas
from fastapi import Depends
from app.routers import deps
from app.database.session import db_session
from fastapi.encoders import jsonable_encoder

def get_candidate_member_id(member_id:str, room_uuid:str)-> List[str]:
    # 1. get all members by room_id
    mr_member = jsonable_encoder(crud.swipe_card.get_mr_member_by_room_uuid(db=db_session, room_uuid=room_uuid))

    # 2. check if there is any members in matching room
    if mr_member:

        all_mr_member_id_list = [ m["member_id"] for m in mr_member]

        # 3. if yes, query MR_Liked_Hated_Member table by member_id
        mr_liked_hated_member = jsonable_encoder(crud.swipe_card.get_preference_by_member_id_and_room_uuid(db=db_session, member_id=member_id, room_uuid=room_uuid))
        rcmd_member_id = [rcmd_member["target_member_id"] for rcmd_member in mr_liked_hated_member]

        # 4. compare it with all the members in matching room to get those who are not recommended
        unrcmd_member_id = set(all_mr_member_id_list) - set(rcmd_member_id) - set([int(member_id)])
        if unrcmd_member_id:
            candidate_member_id_list = list(unrcmd_member_id)
        else:
            candidate_member_id_list = []

    else:
        candidate_member_id_list = []
        
    return candidate_member_id_list

class RecommendationFeature(ABC):
    """
    feature interface
    """
    @abstractmethod
    def prepare(self, member_id:str, room_uuid:str) -> Any:
        pass

class RandomRecommendFeature:
    def prepare(self, member_id:str, room_uuid:str) -> List[str]:
        candidate_member_id_list = get_candidate_member_id(member_id, room_uuid)
        return candidate_member_id_list

class HotPersonRecommendFeature:
    def prepare(self, member_id:str, room_uuid:str) ->  Tuple[List[str], Tuple[str, str]]:
        candidate_member_id_list = get_candidate_member_id(member_id, room_uuid)
        # other features
        pass