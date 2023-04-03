from fastapi import APIRouter

from app.routers.api_v1 import user, login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
