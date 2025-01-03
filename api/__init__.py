from fastapi import APIRouter, Request
from starlette.responses import FileResponse
from .auth import sub_router

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
def favicon(request: Request):
    request.state.islogsave = False
    return FileResponse("static/favicon.ico")


router.include_router(sub_router)

__all__ = ["router"]
