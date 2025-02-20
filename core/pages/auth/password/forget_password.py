import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import APIRouter, Response, Depends
from fastapi.responses import HTMLResponse
from core import config_auth, config
from core.pages.response import PageResponse, EnumJS
from fastapi.exceptions import RequestValidationError
from core.app.auth.user.service import UserQueryService, UserCommandService
from core.app.security.client.service import ClientService
from core.app.security.clientsso.service import ClientSSOService
from core.app.security.client.exceptions import ClientNotFoundException
from core.app.security.client.service import ClientUserResetService
from ..logout.logout import page_auth_logout
from .request import ForgetPasswordRequest, ForgetPasswordGantiRequest
from core.utils import fonnte_bot_sendtext

router = APIRouter(prefix="/forget_password")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_auth_forget_password(req: page_req, res: Response, client_id: str = None):
    print("page_auth_forget_password")
    title_form = config.APP_NAME
    if client_id is not None:
        data_clientsso = await ClientSSOService().get_clientsso(client_id)
        if data_clientsso is None:
            return await page_auth_logout(res, req)
        title_form = data_clientsso.nama
    else:
        client_id = "-"
    page.addContext("clientsso_id", client_id)
    page.addContext("title_form", title_form)
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse)
async def page_auth_forget_password_js(req: page_req, pathFile: EnumJS, client_id: str = None, salt: str = None):
    if client_id is None or client_id == "None":
        client_id = "-"
    page.addContext("clientsso_id", client_id)
    page.addContext("client_id", req.user.client_id)
    page.addContext("salt", salt)
    return page.response(req, "/html/" + pathFile)


@router.get("/{salt}", response_class=HTMLResponse)
async def page_auth_forget_password(request: page_req, response: Response, salt: str = None):
    title_form = config.APP_NAME
    data_reset = await ClientUserResetService().get_clientusers_reset_by_salt(salt)
    if data_reset is None:
        return await page_auth_logout(response, request)

    data_user = await UserQueryService().get_user_by(username=data_reset.user)
    if data_user is None:
        return await page_auth_logout(response, request)

    page.addContext("title_form", title_form)
    page.addContext("data_user", data_user)
    page.addContext("salt", salt)
    return page.response(request, "/html/form.html")


@router.post("/{PathCheck}", status_code=201)
async def page_auth_forget_password_request(dataIn: ForgetPasswordRequest, req: page_req, res: Response):  #
    #### Cek Client ID
    data_client = await ClientService().get_client_id(dataIn.client_id)
    if data_client is None:
        raise ClientNotFoundException
    if data_client.disabled:
        errors = [{"loc": ["body", "email"], "msg": f'client "{data_client.client_id}" di disable', "type": ""}]
        raise RequestValidationError(errors)
    if dataIn.client_id != req.user.client_id:
        errors = [{"loc": ["body", "email"], "msg": f"client tidak terdaftar", "type": ""}]
        raise RequestValidationError(errors)

    #### Cek User
    data_user = await UserQueryService().get_user_by(email=dataIn.email)
    if not data_user:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"email {dataIn.email} tidak terdaftar", "type": ""}])
    if data_user.disabled:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"akun telah di disabled", "type": ""}])

    data_clientsso_reset = await ClientUserResetService().get_clientusers_reset(data_user.username)
    if data_clientsso_reset is not None:
        if data_clientsso_reset.active:
            raise RequestValidationError([{"loc": ["body", "email"], "msg": f"kode reset password sudah diterbitkan", "type": ""}])

    data_clientsso_reset = await ClientUserResetService().create_clientuser_reset(data_user.username)

    reset_url = f"{config.HOST_URL}/auth/forget_password/{data_clientsso_reset.salt}"
    await fonnte_bot_sendtext(message_key="reset_code", target=data_user.nohp, data={"code": data_clientsso_reset.code, "link": reset_url})
    sleep(5)
    return {"redirect_uri": f"{reset_url}"}  # Redirect to callback


@router.post("/{PathCheck}/{salt}", status_code=201)
async def page_auth_forget_password_ganti(dataIn: ForgetPasswordGantiRequest, request: page_req, response: Response, salt: str = None):  #
    data_reset = await ClientUserResetService().get_clientusers_reset_by_salt(salt)
    if data_reset is None:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"permintaan reset tidak tersedia", "type": ""}])

    data_user = await UserQueryService().get_user_by(username=data_reset.user)
    if data_user is None:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"akun tidak tersedia", "type": ""}])

    if dataIn.email != data_user.email:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"data reset tidak cocok", "type": ""}])

    if data_reset.code != dataIn.code:
        raise RequestValidationError([{"loc": ["body", "code"], "msg": f"kode reset tidak cocok", "type": ""}])

    if dataIn.password != dataIn.password2:
        raise RequestValidationError([{"loc": ["body", "password"], "msg": "password tidak sama", "type": "value_error.duplicate"}])

    await ClientUserResetService().delete_clientusers_reset(data_user.username)

    sleep(1)
    await UserCommandService().update_user_password(data_user.id, dataIn.password, dataIn.password2)
    await fonnte_bot_sendtext(
        message_key="password_change",
        target=data_user.nohp,
        data={"full_name": data_user.full_name, "tanggal": datetime.now().strftime("%d %B %Y %H:%M")},
    )

    return {"redirect_uri": f"/auth/login"}  # Redirect to callback
