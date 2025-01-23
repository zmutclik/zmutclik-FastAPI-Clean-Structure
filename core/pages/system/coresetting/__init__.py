from fastapi import APIRouter

from .coresetting import router as coresystem_router_
from .crossorigin import router as crossorigin_router
from .changelog import router as changelog_router

coresystem_router = APIRouter()
coresystem_router.include_router(coresystem_router_, tags=["SYS / CORESYSTEM"])
coresystem_router.include_router(crossorigin_router, tags=["SYS / CORESYSTEM"])
coresystem_router.include_router(changelog_router, tags=["SYS / CORESYSTEM"])


__all__ = ["coresystem"]
