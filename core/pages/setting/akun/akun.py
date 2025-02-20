import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from core.pages.response import PageResponse, EnumJS

from core.app.auth.user.service import UserQueryService, UserCommandService
from core.app.auth.privilege.service import PrivilegeQueryService
from core.app.auth.scope.service import ScopeQueryService

from .request import AkunRequest
from .response import AkunResponse

router = APIRouter(prefix="/akun")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/settings" + router.prefix, depend_roles=["admin"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_settings_akun(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_settings_akun_form_add(req: page_req):
    user__ = await UserQueryService().get_user_by(username=req.user.username)
    userp_ = await UserQueryService().get_user_privilege(user__.id, 3)

    page.addContext("data_privileges", await PrivilegeQueryService().get_privileges(userp_ is not None))
    page.addContext("data_scopes", await ScopeQueryService().get_scopes())
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{user_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_settings_akun_form_edit(user_id: int, req: page_req):
    user__ = await UserQueryService().get_user_by(username=req.user.username)
    userp_ = await UserQueryService().get_user_privilege(user__.id, 3)

    data_user_privileges = []
    for item in await UserQueryService().get_user_privileges(user_id):
        data_user_privileges.append(item.privilege_id)
    data_user_scopes = []
    for item in await UserQueryService().get_user_scopes(user_id):
        data_user_scopes.append(item.scope_id)

    page.addContext("data_privileges", await PrivilegeQueryService().get_privileges(userp_ is not None))
    page.addContext("data_user_privileges", data_user_privileges)
    page.addContext("data_scopes", await ScopeQueryService().get_scopes())
    page.addContext("data_user_scopes", data_user_scopes)
    page.addContext("data_user", await UserQueryService().get_user(user_id))
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_settings_akun_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def page_settings_akun_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await UserQueryService().datatable(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=AkunResponse, dependencies=page.depend_w())
async def page_settings_akun_create(dataIn: AkunRequest, req: page_req):
    await UserQueryService().validate_user(dataIn.username, dataIn.email, dataIn.nohp)

    data_created = await UserCommandService().create_user(
        created_user="",
        username=dataIn.username,
        email=dataIn.email,
        full_name=dataIn.full_name,
        nohp=dataIn.nohp,
    )
    return data_created


@router.post("/{PathCheck}/{user_id}/reset", status_code=201, dependencies=page.depend_w())
async def page_settings_akun_send_reset_password(user_id: int, req: page_req):
    from core.app.security.client.service import ClientUserResetService
    from core import config
    from core.utils import fonnte_bot_sendtext

    data_user = await UserQueryService().get_user(user_id)
    await ClientUserResetService().delete_clientusers_reset(data_user.username)
    data_clientsso_reset = await ClientUserResetService().create_clientuser_reset(data_user.username)
    reset_url = f"{config.HOST_URL}/auth/forget_password/{data_clientsso_reset.salt}"
    await fonnte_bot_sendtext(message_key="reset_code", target=data_user.nohp, data={"code": data_clientsso_reset.code, "link": reset_url})


@router.post("/{PathCheck}/{user_id:int}", status_code=201, response_model=AkunResponse, dependencies=page.depend_w())
async def page_settings_akun_update(user_id: int, dataIn: AkunRequest, req: page_req):
    data_get = await UserQueryService().get_user(user_id)
    data_update = {}
    if dataIn.username != data_get.username:
        data_update["username"] = dataIn.username
    if dataIn.email != data_get.email:
        data_update["email"] = dataIn.email
    if dataIn.nohp != data_get.nohp:
        data_update["nohp"] = dataIn.nohp

    await UserQueryService().validate_user(**data_update)

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
async def page_settings_akun_delete(user_id: int, req: page_req):
    await UserQueryService().get_user(user_id)
    await UserCommandService().delete_user(user_id, req.user.username)
