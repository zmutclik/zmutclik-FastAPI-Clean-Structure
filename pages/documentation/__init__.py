from fastapi import APIRouter

from .documentation import router

documentation_router = APIRouter()
documentation_router.include_router(router, tags=["DOCUMENTATION"])


__all__ = ["documentation_router"]
