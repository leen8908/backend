from abc import ABC, abstractmethod


class RecommendationStrategy(ABC):
    """
    Swipe card 推薦演算法抽象策略 class
    """

    @abstractmethod
    def recommend(self, member_id, room_id):
        raise NotImplementedError()


class RandomRecommendation(RecommendationStrategy):
    """
    Swipe card 随機推薦演算法策略 class
    """

    def recommend(self, member_id, room_id):
        """
        implement random recommendation
        """

        # 1. get all members by room_id
        # 2. check if there is any members in matching room
        # 3. if yes, query MR_Liked_Hated_Member table by member_id
        # 4. compare it with all the members in matching room to get those who are not recommended
        ##以上應該會用adapter另外用crud
        # 5. randomly get 5 members
        # 6. use the member_id and room_id to get self tag text and find tag text, and make a recommendation list

        # return recommendation list

# 先決定要傳入的資料結構(可以從其他推薦演算法來想怎樣可以最符合各種情況的資料結構)!再來決定Crud要怎麼寫
# crud ,adapter, algorithm
# adapter 可以讓不同algorithm去用同樣的crud