from abc import ABC, abstractmethod
from typing import List, Tuple

from .recommendation_feature import RecommendationFeature, RandomRecommendFeature, HotPersonRecommendFeature

class FeatureContainerFactory(ABC):
    """
    抽象feature container 工廠
    """
    @abstractmethod
    def create_feature_container(self) -> RecommendationFeature:
        pass

class RandomFeatureFactory(FeatureContainerFactory):
    def create_feature_container(self) -> RandomRecommendFeature:
        return RandomRecommendFeature()

class HotPersonFeatureFactory(FeatureContainerFactory):
    def create_feature_container(self) -> HotPersonRecommendFeature:
       
        return HotPersonRecommendFeature()
