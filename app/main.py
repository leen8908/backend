from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils import get_tw_time
from app.core.config import settings
from app.routers.api_v1.api import api_router
#from app.routers.api_v1 import auth
from starlette.responses import HTMLResponse
from starlette.requests import Request

app = FastAPI(title=settings.APP_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json)")

origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
#app.mount("/app/routers/api/v1/auth",auth.auth_app )

@app.get("/api/healthchecker")
def read_root():
    return {"msg": "Hello World"}


@app.get("/api/basicinfo")
def get_info():
    return {"app_name": settings.APP_NAME, "time": get_tw_time()}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
