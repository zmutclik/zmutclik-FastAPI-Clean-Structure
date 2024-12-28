from fastapi import APIRouter

from .me import auth_me_router

sub_router = APIRouter()
sub_router.include_router(auth_me_router, prefix="/api/me", tags=["AUTH"])


__all__ = ["sub_router"]
