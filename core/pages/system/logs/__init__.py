from fastapi import APIRouter

from .logs import router

logs_router = APIRouter()
logs_router.include_router(router, tags=["SETTINGS / LOGS"])


__all__ = ["logs_router"]
