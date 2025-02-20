from fastapi import APIRouter

from .forget_password import router

forget_router = APIRouter()
forget_router.include_router(router, tags=["AUTH / FORGET PASSWORD"])


__all__ = ["forget_router"]
