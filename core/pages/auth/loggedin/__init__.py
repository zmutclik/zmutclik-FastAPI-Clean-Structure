from fastapi import APIRouter

from .loggedin import router

loggedin_router = APIRouter()
loggedin_router.include_router(router, tags=["AUTH / LOGGEDIN"])


__all__ = ["loggedin_router"]
