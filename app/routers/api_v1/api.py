from fastapi import APIRouter

from app.routers.api_v1 import (
    auth,
    group,
    login,
    matching_room,
    notification,
    search,
    user,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.mount("/google-auth", auth.auth_app)
api_router.include_router(
    matching_room.router, prefix="/matching-room", tags=["matching-room"]
)
api_router.include_router(group.router, prefix="/group", tags=["group"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(
    notification.router, prefix="/notification", tags=["notification"]
)
