from typing import List

from app.schemas import SwipeCard


class RecommendationContext:
    """
    推薦演算法 context class
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def recommend(self, member_id, room_id) -> List[SwipeCard]:
        # 調用當前策略的推薦演算法
        return self.strategy.recommend(member_id, room_id)
