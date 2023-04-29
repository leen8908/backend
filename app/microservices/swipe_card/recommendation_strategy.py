from abc import ABC, abstractmethod
from typing import List
import random
# from .prepare_recommendation import PrepareRandomRecommend, PrepareHotguyRecommend
# from .adapter import RandomAdapter
from .recommend_feature_factory import RandomFeatureFactory, HotPersonFeatureFactory
from .recommend_feature_prepare import RecommendFeaturePreparer


class RecommendationStrategy(ABC):
    """
    Swipe card 推薦演算法抽象策略 class
    """

    @abstractmethod
    def recommend(self, member_id, room_uuid) -> List[str]:
        pass


class RandomRecommendation(RecommendationStrategy):
    """
    Swipe card 随機推薦演算法策略 class
    """

    def recommend(self, member_id, room_uuid):
        """
        implement random recommendation
        """
        # get candidate member_id list:
        # prepare_random_recommend = PrepareRandomRecommend()
        # prepare_random_recommend__adapter = RandomAdapter(prepare_random_recommend)
        # candidate_member_id_list = prepare_random_recommend__adapter.prepare(member_id, room_uuid)
        random_feature_preparer = RecommendFeaturePreparer(RandomFeatureFactory())
        candidate_member_id_list = random_feature_preparer.feature_order(member_id, room_uuid) #回傳一個 member_id list
        
        # Recommend Algorithm: randomly get 5 members
        if len(candidate_member_id_list) != 0:
            random.shuffle(candidate_member_id_list)
            return candidate_member_id_list[:5]

        else:
            return []
            

        # return member_id recommendation list

# 先決定要傳入的資料結構(可以從其他推薦演算法來想怎樣可以最符合各種情況的資料結構)!再來決定Crud要怎麼寫
# crud ,adapter, algorithm
# adapter 可以讓不同algorithm去用同樣的crud

class HotPersonRecommendation(RecommendationStrategy):
    """
    Swipe card 優先推夯哥夯姊推薦演算法策略 class
    """
    def recommend(self, member_id, room_uuid) -> List[str]:
        # get candidate member_id list:
        hot_guy_preparer = RecommendFeaturePreparer(HotPersonFeatureFactory())
        recommend_feature = hot_guy_preparer.feature_order(member_id, room_uuid)

        # Recommend Algorithm:
        # recommend_feature = {"candidate_member_id", 
        #                      "",
        #                      }
        
        pass