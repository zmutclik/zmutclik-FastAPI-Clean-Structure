from fastapi import APIRouter
from api.auth import sub_router
# from api.user.v1 import sub_router as user_v1_router

router = APIRouter()
router.include_router(sub_router)


__all__ = ["router"]