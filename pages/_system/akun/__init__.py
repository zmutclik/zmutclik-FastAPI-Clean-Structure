from fastapi import APIRouter

from .akun import akun_router

akun_routers = APIRouter()
akun_routers.include_router(akun_router, tags=["SYS / AKUN"])


__all__ = ["akun_routers"]
