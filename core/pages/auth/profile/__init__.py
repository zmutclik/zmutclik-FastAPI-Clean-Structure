from fastapi import APIRouter

from .profile import router

profile_router = APIRouter()
profile_router.include_router(router, tags=["AUTH / PROFILE"])


__all__ = ["profile_router"]
