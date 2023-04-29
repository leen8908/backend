# from abc import ABC, abstractmethod
# from typing import List
# from .recommendation_feature import PrepareRandomRecommend, PrepareHotguyRecommend


# class PrepareRecommendation(ABC):
#     """
#     準備推薦演算法會用到的特徵的 target class
#     """

#     @abstractmethod
#     def prepare(self, member_id, room_uuid):
#         pass

# class RandomAdapter(PrepareRecommendation):
#     """
#     準備 Random 推薦演算法的特徵的 Adaptee class
#     """
#     def __init__(self, prepare_random_recommendation: PrepareRandomRecommend):
#         self.prepare_random_recommendation = prepare_random_recommendation

#     def prepare(self, member_id:str, room_uuid:str) -> List[str]:
#         candidate_member_id_list = self.prepare_random_recommendation.prepare_candidate_member_id(member_id,room_uuid)
#         return candidate_member_id_list
    
# class HotGuyAdapter(PrepareRecommendation):
#     """
#     準備 Hot guy 推薦演算法的特徵的 Adaptee class
#     """
#     def __init__(self, prepare_hot_guy_recommendation: PrepareHotguyRecommend):
#         self.prepare_hot_guy_recommendation = prepare_hot_guy_recommendation

#     def prepare(self, member_id:str, room_uuid:str):
#         candidate_member_id_with_feature_list = self.prepare_hot_guy_recommendation.prepare_candidate_member_id_with_feature(member_id,room_uuid)
#         return candidate_member_id_with_feature_list