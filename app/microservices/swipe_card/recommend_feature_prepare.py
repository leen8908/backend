from .recommend_feature_factory import FeatureContainerFactory
from typing import Any

class RecommendFeaturePreparer:
    def __init__(self, feature_container_factory: FeatureContainerFactory) -> None:
        self.feature_container_factory = feature_container_factory

    def feature_order(self, member_id:str, room_uuid:str) -> Any:
        recommend_feature = self.feature_container_factory.create_feature_container()
        return recommend_feature.prepare(member_id, room_uuid)