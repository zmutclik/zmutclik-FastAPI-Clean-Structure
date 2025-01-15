from fastapi import APIRouter

from .akun import akun_router
from .privilege import privilege_router

system_router = APIRouter()
system_router.include_router(akun_router)
system_router.include_router(privilege_router)


__all__ = ["system_router"]
