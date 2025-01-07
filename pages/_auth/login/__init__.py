from fastapi import APIRouter

from .login import login_router

login_routers = APIRouter()
login_routers.include_router(login_router, tags=["AUTH"])


__all__ = ["login_routers"]
