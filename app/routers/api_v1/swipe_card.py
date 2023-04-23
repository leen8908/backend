from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.microservices.swipe_card.recommendation_context import RecommendationContext
from app.microservices.swipe_card.recommendation_strategy import RandomRecommendation
from app.routers import deps

router = APIRouter()
# create RecommendationContext instance
recommendation_context = RecommendationContext()
# Create recommend strategy instance
random_recommendation_strategy = RandomRecommendation()


@router.post("/swipe", response_model=schemas.user.UserMessage)
def save_preference(
    *,
    db: Session = Depends(deps.get_db),
    swiped_card_in: schemas.SwipeCardPreference,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Save member's preference from the card he swiped.
    """


@router.post(
    "/swipe-recommend", response_model=schemas.swipe_card.ReturnSwipeCardMessage
)
def get_recommendation(
    *,
    db: Session = Depends(deps.get_db),
    recommend_in: schemas.SwipeCardRecommend,  # member_id, room_id
) -> Any:
    """
    return a swipe card recommenation list
    """
    recommendation_context.set_strategy(random_recommendation_strategy)
    recommend_list = recommendation_context.recommend(
        recommend_in.member_id, recommend_in.room_id
    )

    return {"message": "success", "data": recommend_list}
