import os
from enum import Enum
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

from core.app.auth.user.exceptions import DuplicateEmailOrNicknameOrNoHPException
from core.app.auth.user.service import UserQueryService, UserCommandService
from core.app.auth.privilege.service import PrivilegeQueryService
from core.app.auth.scope.service import ScopeQueryService

from .request import AkunRequest
from .response import AkunResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/akun")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/settings" + router.prefix, depend_roles=["admin"])
page_req = Annotated[PageResponse, Depends(page.request)]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_settings_akun(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_settings_akun_form_add(req: page_req):
    page.addContext("data_privileges", await PrivilegeQueryService().get_privileges())
    page.addContext("data_scopes", await ScopeQueryService().get_scopes())
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{user_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_settings_akun_form_edit(user_id: int, req: page_req):
    data_user_privileges = []
    for item in await UserQueryService().get_user_privileges(user_id):
        data_user_privileges.append(item.privilege_id)
    data_user_scopes = []
    for item in await UserQueryService().get_user_scopes(user_id):
        data_user_scopes.append(item.scope_id)

    page.addContext("data_privileges", await PrivilegeQueryService().get_privileges())
    page.addContext("data_user_privileges", data_user_privileges)
    page.addContext("data_scopes", await ScopeQueryService().get_scopes())
    page.addContext("data_user_scopes", data_user_scopes)
    page.addContext("data_user", await UserQueryService().get_user(user_id))
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_js_akun(req: page_req, pathFile: PathJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def datatables_akun(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await UserQueryService().datatable(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=AkunResponse, dependencies=page.depend_w(), deprecated=True)
async def create_user_akun(dataIn: AkunRequest, req: page_req):
    data_get = await UserQueryService().get_user_by(username=dataIn.username, email=dataIn.email, nohp=dataIn.nohp)
    if data_get is not None:
        raise DuplicateEmailOrNicknameOrNoHPException

    data_created = await UserCommandService().create_user(
        created_user="", username=dataIn.username, email=dataIn.email, full_name=dataIn.full_name, nohp=dataIn.nohp
    )
    return data_created


@router.post("/{PathCheck}/{user_id:int}", status_code=201, response_model=AkunResponse, dependencies=page.depend_w())
async def update_akun(user_id: int, dataIn: AkunRequest, req: page_req):
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
        privileges=dataIn.privileges,
        scopes=dataIn.scopes,
    )
    return data_updated


@router.delete("/{PathCheck}/{user_id:int}", status_code=202, dependencies=page.depend_d())
async def delete_akun(user_id: int, req: page_req):
    await UserQueryService().get_user(user_id)
    await UserCommandService().delete_user(user_id, req.user.username)
