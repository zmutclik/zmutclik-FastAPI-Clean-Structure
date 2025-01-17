from fastapi import APIRouter

from .register import router

register_router = APIRouter()
register_router.include_router(router, tags=["AUTH"])


__all__ = ["register_router"]
