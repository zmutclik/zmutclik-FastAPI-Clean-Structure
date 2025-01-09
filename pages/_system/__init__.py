from fastapi import APIRouter

from .akun import akun_router

system_router = APIRouter()
system_router.include_router(akun_router)


__all__ = ["system_router"]
