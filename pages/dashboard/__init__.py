from fastapi import APIRouter

from .dashboard import router

dashboard_router = APIRouter()
dashboard_router.include_router(router, tags=["DASHBOARD"])


__all__ = ["dashboard_router"]
