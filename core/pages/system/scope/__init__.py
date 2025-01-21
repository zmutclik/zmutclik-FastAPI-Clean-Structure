from fastapi import APIRouter

from .scope import router

scope_router = APIRouter()
scope_router.include_router(router, tags=["SYS / SCOPE"])


__all__ = ["scope_router"]
