from fastapi import APIRouter

from .akun import router

akun_router = APIRouter()
akun_router.include_router(router, tags=["SYS / AKUN"])


__all__ = ["akun_router"]
