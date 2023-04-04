from fastapi import APIRouter

from app.routers.api_v1 import user, login, matching_room, group, search

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(matching_room.router,
                          prefix="/matching-room", tags=["matching-room"])
api_router.include_router(group.router, prefix="/groups", tags=["groups"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
