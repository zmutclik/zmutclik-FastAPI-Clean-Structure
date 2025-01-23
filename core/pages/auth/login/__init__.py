from fastapi import APIRouter

from .login import router

login_router = APIRouter()
login_router.include_router(router, tags=["AUTH / LOGIN"])


__all__ = ["login_router"]
