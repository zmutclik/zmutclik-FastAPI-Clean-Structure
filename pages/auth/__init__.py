from fastapi import APIRouter

from .login import login_routers

auth_router = APIRouter()
auth_router.include_router(login_routers)


__all__ = ["login_routers"]
