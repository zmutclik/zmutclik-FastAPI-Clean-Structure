from fastapi import APIRouter
from .session import router

session_router = APIRouter()
session_router.include_router(router, tags=["SETTINGS / SESSION"])


__all__ = ["session_router"]
