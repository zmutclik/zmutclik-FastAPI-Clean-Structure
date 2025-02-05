import os
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

from core.app.auth.user.service import UserQueryService, UserCommandService
from core.app.auth.user.exceptions import UserNotFoundException

from .request import SettingProfileRequest, GantiPasswordRequest
from fastapi.exceptions import RequestValidationError
from time import sleep

router = APIRouter(prefix="/profile")
page = PageResponse(
    path_template=os.path.dirname(__file__),
    prefix_url="/auth" + router.prefix,
    depend_roles=["system"],
)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.dependencies())
async def page_auth_profile(req: page_req):
    page.addContext("data_user", await UserQueryService().get_user_by(username=req.user.username))
    return page.response(req, "/html/index.html")


@router.get(
    "/{PathCheck}/ganti_password.js",
    response_class=HTMLResponse,
    dependencies=page.dependencies(),
)
async def page_auth_profile_js_ganti_password(req: page_req):
    return page.response(req, "/html/ganti_password.js")


@router.get(
    "/{PathCheck}/setting.js",
    response_class=HTMLResponse,
    dependencies=page.dependencies(),
)
async def page_auth_profile_js_setting(req: page_req):
    return page.response(req, "/html/setting.js")


#######################################################################################################################
@router.post("/{PathCheck}/gantipassword", status_code=201)
async def page_auth_profile_save_ganti_password(dataIn: GantiPasswordRequest, req: page_req):
    data_get = await UserQueryService().get_user_by(req.user.username)
    if data_get is None:
        raise UserNotFoundException

    if not await UserQueryService().verify_password(user=data_get, plain_password=dataIn.password_lama):
        errors = [{"loc": ["body", "password_lama"], "msg": "password lama gagal dicocokkan", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)
    if dataIn.password_baru1 != dataIn.password_baru2:
        errors = [{"loc": ["body", "password_baru2"], "msg": "password baru tidak sama", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    sleep(1)
    await UserCommandService().update_user_password(data_get.id, dataIn.password_baru1, dataIn.password_baru2)


@router.post("/{PathCheck}/setting", status_code=201)
async def page_auth_profile_save_setting(dataIn: SettingProfileRequest, req: page_req):
    data_get = await UserQueryService().get_user_by(req.user.username)
    if data_get is None:
        raise UserNotFoundException

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

    sleep(1)
    await UserCommandService().update_user(
        user_id=data_get.id,
        email=dataIn.email,
        nohp=dataIn.nohp,
        full_name=dataIn.full_name,
    )
