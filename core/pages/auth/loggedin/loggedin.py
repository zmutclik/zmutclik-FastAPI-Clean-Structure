import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse

from core import config_auth, config
from core.fastapi.helper import get_ipaddress, set_refresh_cookies, set_token_cookies
from ..logout.logout import page_auth_logout
from core.pages.response import PageResponse
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.auth.user.exceptions import UserNotFoundException
from core.app.security.client.exceptions import ClientNotFoundException
from core.app.security.client.service import ClientUserOTPService, ClientService, ClientUserService
from core.app.security.clientsso.service import ClientSSOService
from core.app.security.clientsso.exceptions import ClientSSONotFoundException
from fastapi.exceptions import RequestValidationError

from .request import OtpRequest, OtpLoginRequest
from core.utils import fonnte_bot_sendtext

router = APIRouter(prefix="/loggedin")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_auth_loggedin(response: Response, request: page_req, redirect_uri: str = None, client_id: str = None):
    data_clientusers = await ClientUserService().get_clientusers(request.user.client_id)
    if data_clientusers is None:
        return await page_auth_logout(response, request, "/auth/login")
    data_users = []
    for data in data_clientusers:
        data_user = await UserQueryService().get_user_by(username=data.user)
        if data_user is not None:
            data_users.append(data_user)
    if data_users == []:
        return await page_auth_logout(response, request, "/auth/login")
    page.addContext("redirect_uri", redirect_uri)
    page.addContext("data_users", data_users)

    ###################################################################################################################
    title_form = config.APP_NAME
    if client_id is not None:
        data_clientsso = await ClientSSOService().get_clientsso(client_id)
        if data_clientsso is None or redirect_uri is None:
            return await page_auth_logout(response, request)
        if data_clientsso.callback_uri != redirect_uri:
            return await page_auth_logout(response, request)
        title_form = data_clientsso.nama
    else:
        client_id = "-"

    if redirect_uri is None or redirect_uri == "None":
        redirect_uri = "/page/dashboard"

    page.addContext("redirect_uri", redirect_uri)
    page.addContext("clientsso_id", client_id)
    page.addContext("title_form", title_form)
    ###################################################################################################################
    return page.response(request, "/html/index.html")


@router.get("/{PathCheck}.js")
async def page_auth_loggedin_js(req: page_req, client_id: str = None):
    if client_id is None or client_id == "None":
        client_id = "-"
    page.addContext("clientsso_id", client_id)
    return page.response(req, "/html/index.js")


async def req_check(email: str, client_id: str):
    data_user = await UserQueryService().get_user_by(email=email)
    if data_user is None:
        raise UserNotFoundException
    data_client = await ClientService().get_client_id(client_id)
    if data_client is None:
        raise ClientNotFoundException
    data_clientuser = await ClientUserService().get_clientuser(data_client.id, data_user.username)
    if data_clientuser is None:
        raise ClientNotFoundException
    data_otp = await ClientUserOTPService().get_clientusers_otp(client_id, data_user.username)
    return data_client, data_user, data_otp


@router.post("/{PathCheck}/check", status_code=201)
async def page_auth_loggedin_send_otp(dataIn: OtpRequest, req: page_req):
    data_client, data_user, data_otp = await req_check(dataIn.email, req.user.client_id)
    if data_otp is None:
        token_time = datetime.now(timezone.utc) + timedelta(minutes=5)
        data_clientusers_otp = await ClientUserOTPService().create_clientuser(data_client.client_id, data_user.username, token_time)
        await fonnte_bot_sendtext(message_key="otp", target=data_user.nohp, data={"code": data_clientusers_otp.otp})
        sleep(4)
    else:
        raise RequestValidationError([{"loc": ["body", "otp"], "msg": f"Kode OTP sudah diterbitkan...", "type": ""}])
    sleep(1)


@router.post("/{PathCheck}/login", status_code=201)
async def page_auth_loggedin_login(dataIn: OtpLoginRequest, req: page_req, res: Response):
    data_client, data_user, data_otp = await req_check(dataIn.email, req.user.client_id)
    if data_otp is not None:
        if data_otp.otp != dataIn.code:
            raise RequestValidationError([{"loc": ["body", "otp"], "msg": f"Kode OTP tidak Cocok", "type": ""}])
        if data_otp.user != data_user.username:
            raise RequestValidationError([{"loc": ["body", "otp"], "msg": f"akun OTP tidak Cocok", "type": ""}])

        await ClientUserOTPService().delete_clientusers_otp(data_client.id, data_user.username)

        if dataIn.client_id is not None:
            data_clientsso = await ClientSSOService().get_clientsso(dataIn.client_id)
            if data_clientsso is None:
                raise ClientSSONotFoundException
            redirect_uri = data_clientsso.callback_uri
            clientsso_id = data_clientsso.clientsso_id
        else:
            clientsso_id = config_auth.SSO_CLIENT_ID
            redirect_uri = "/auth/callback"

        data_clientsso_code = await ClientSSOService().create_clientsso_code(clientsso_id, data_user.id, req.user.client_id)
        sleep(1)
        return {"redirect_uri": f"{redirect_uri}?code={data_clientsso_code.code}"}  # Redirect to callback
