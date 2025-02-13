from fastapi import APIRouter

from .client_sso import router

clientsso_router = APIRouter()
clientsso_router.include_router(router, tags=["SYS / CLIENT-SSO"])


__all__ = ["clientsso_router"]
