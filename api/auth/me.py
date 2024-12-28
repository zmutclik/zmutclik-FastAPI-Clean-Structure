from fastapi import APIRouter, Depends, Request

from app._sys.user.service import UserQueryService, UserCommandService

from core.fastapi.schemas.response import ExceptionResponseSchema
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated

auth_me_router = APIRouter()


@auth_me_router.get(
    "",
    # response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    summary="Get User",
)
async def get_user(req: Request):
    return await UserQueryService().get_user(user_id=req.user.id)
