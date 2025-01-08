import os
from time import sleep
from enum import Enum
from typing import Annotated, Any
from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from pages.response import PageResponse
from app._sys.user.service import UserQueryService, UserCommandService
from app._sys.user.exceptions import (
    UserNotFoundException,
    DuplicateEmailOrNicknameOrNoHPException,
)
from core.fastapi.dependencies import PermissionDependency, RoleDependency, IsAuthenticated, ScopeDependency
from core.exceptions import RequiresLoginException
from pages._system.akun.request import AkunRequest
from pages._system.akun.response import AkunResponse
from fastapi.exceptions import RequestValidationError

akun_router = APIRouter(prefix="/sys/akun")
page = PageResponse(os.path.dirname(__file__), akun_router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]

depend_redirect_url = "/page/sys/akun"
depend_r = [
    Depends(PermissionDependency(permissions=[IsAuthenticated], exception=RequiresLoginException)),
    Depends(RoleDependency("user", exception=RequiresLoginException(depend_redirect_url))),
    Depends(ScopeDependency(["read"], exception=RequiresLoginException(depend_redirect_url))),
]
depend_w = [
    Depends(PermissionDependency(permissions=[IsAuthenticated])),
    Depends(RoleDependency("user", exception=RequiresLoginException(depend_redirect_url))),
    Depends(ScopeDependency(["read", "write"], exception=RequiresLoginException(depend_redirect_url))),
]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


@akun_router.get("", response_class=HTMLResponse, dependencies=depend_r)
async def page_akun(req: page_req):
    return page.response(req, "/html/index.html")


@akun_router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=depend_w)
async def page_akun(req: page_req):
    return page.response(req, "/html/form.html")


@akun_router.get("/{PathCheck}/{id:int}", response_class=HTMLResponse, dependencies=depend_w)
async def page_akun(id: int, req: page_req):
    page.addContext("data_user", await UserQueryService().get_user(id))
    return page.response(req, "/html/form.html")


@akun_router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=depend_r)
async def page_akunjs(req: page_req, pathFile: PathJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@akun_router.post("/{PathCheck}/datatables", status_code=202, dependencies=depend_r)
async def get_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await UserQueryService().datatable(params=params)


@akun_router.post("/{PathCheck}", status_code=201, response_model=AkunResponse, dependencies=depend_w, deprecated=True)
async def create_user(dataIn: AkunRequest, req: page_req):
    data_get = await UserQueryService().get_user_by(username=dataIn.username, email=dataIn.email, nohp=dataIn.nohp)
    if data_get is not None:
        raise DuplicateEmailOrNicknameOrNoHPException

    data_created = await UserCommandService().create_user(
        created_user="", username=dataIn.username, email=dataIn.email, full_name=dataIn.full_name, nohp=dataIn.nohp
    )
    return data_created


@akun_router.post("/{PathCheck}/{user_id:int}", status_code=201, response_model=AkunResponse, dependencies=depend_w)
async def update_user(user_id: int, dataIn: AkunRequest, req: page_req):
    data_get = await UserQueryService().get_user(user_id)

    if dataIn.username != data_get.username:
        data_filter = await UserQueryService().get_user_by(username=dataIn.username)
        if data_filter is not None:
            errors = [{"loc": ["body", "username"], "msg": "duplicate username is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    if dataIn.email != data_get.email:
        data_filter = await UserQueryService().get_user_by(email=dataIn.email)
        if data_filter is not None:
            errors = [{"loc": ["body", "email"], "msg": "duplicate email is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    if dataIn.nohp != data_get.nohp:
        data_filter = await UserQueryService().get_user_by(nohp=dataIn.nohp)
        if data_filter is not None:
            errors = [{"loc": ["body", "nohp"], "msg": "duplicate nohp is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await UserCommandService().update_user(
        user_id=user_id,
        username=dataIn.username,
        email=dataIn.email,
        nohp=dataIn.nohp,
        full_name=dataIn.full_name,
        disabled=dataIn.disabled,
    )
    return data_updated
