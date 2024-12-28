from fastapi import APIRouter, Depends, Response

from app._sys.user.service import UserQueryService, UserCommandService

from core.fastapi.schemas.response import ExceptionResponseSchema
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated, HasScope

user_router = APIRouter()


@user_router.get(
    "/{user_id}",
    # response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    summary="Get User"
)
async def get_user(user_id: int):
    return await UserQueryService().get_user(user_id=user_id)

