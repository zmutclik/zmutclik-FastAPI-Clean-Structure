from fastapi import APIRouter

from .akun import akun_routers

system_router = APIRouter()
system_router.include_router(akun_routers)


__all__ = ["system_router"]
