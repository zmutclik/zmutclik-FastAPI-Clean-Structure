from fastapi import APIRouter

from .privilege import router

privilege_router = APIRouter()
privilege_router.include_router(router, tags=["SYS / PRIVILEGE"])


__all__ = ["privilege_router"]
