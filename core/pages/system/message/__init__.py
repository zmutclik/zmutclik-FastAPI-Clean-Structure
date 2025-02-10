from fastapi import APIRouter

from .message import router

message_router = APIRouter()
message_router.include_router(router, tags=["SETTINGS / MESSAGE"])


__all__ = ["message_router"]
