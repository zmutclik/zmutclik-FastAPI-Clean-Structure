from fastapi import APIRouter, Depends, Request

from app._sys.user.service import UserQueryService

from core.fastapi.schemas.response import ExceptionResponseSchema
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated

from api.auth.response import GetUserResponse
auth_me_router = APIRouter()


@auth_me_router.get(
    "",
    response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    summary="Get My Data",
)
async def get_user(req: Request):
    return await UserQueryService().get_user(user_id=req.user.id)


from app._sys.crossorigin.service import CrossOriginQueryService
@auth_me_router.get(
    "test",
    response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    summary="Get My Data",
)
async def get_user(req: Request):
    return await CrossOriginQueryService().get_crossorigin_by_id("1")
