from fastapi import APIRouter

from .repository import router

repository_router = APIRouter()
repository_router.include_router(router, tags=["SYS / REPOSITORY"])


__all__ = ["repository_router"]
