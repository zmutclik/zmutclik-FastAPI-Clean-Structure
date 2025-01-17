from fastapi import APIRouter

from .login import login_router
from .register import register_router

auth_router = APIRouter()
auth_router.include_router(login_router)
auth_router.include_router(register_router)


__all__ = ["auth_router"]
