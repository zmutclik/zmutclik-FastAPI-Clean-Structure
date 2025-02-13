import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse

from core import config_auth
from core.fastapi.helper import get_ipaddress, set_refresh_cookies, set_token_cookies
from ..logout.logout import page_auth_logout
from core.pages.response import PageResponse
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.auth.user.exceptions import UserNotFoundException
from core.app.security.client.exceptions import ClientNotFoundException
from core.app.security.client.service import ClientUserOTPService, ClientService, ClientUserService
from fastapi.exceptions import RequestValidationError

from .request import OtpRequest, OtpLoginRequest
from core.utils import fonnte_bot_sendtext

router = APIRouter(prefix="/loggedin")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_auth_loggedin(response: Response, request: page_req, redirect_uri: str = None):
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
    return page.response(request, "/html/index.html")


@router.get("/{PathCheck}.js")
async def page_auth_loggedin_js(redirect_uri: str, req: page_req):
    if redirect_uri is None or redirect_uri == "None":
        redirect_uri = "/page/dashboard"
    page.addContext("redirect_uri", redirect_uri)
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
        token_time = datetime.now(timezone.utc) + timedelta(minutes=10)
        data_clientusers_otp = await ClientUserOTPService().create_clientuser(data_client.client_id, data_user.username, token_time)
        await fonnte_bot_sendtext(message_key="otp", target=data_user.nohp, data={"code": data_clientusers_otp.otp})
        sleep(4)
    sleep(1)


@router.post("/{PathCheck}/login", status_code=201)
async def page_auth_loggedin_login(dataIn: OtpLoginRequest, req: page_req, res: Response):
    data_client, data_user, data_otp = await req_check(dataIn.email, req.user.client_id)
    if data_otp is not None:
        if data_otp.otp != dataIn.code:
            raise RequestValidationError([{"loc": ["body", "otp"], "msg": f"Kode OTP tidak Cocok", "type": ""}])

        await ClientUserOTPService().delete_clientusers_otp(data_client.id, data_user.username)
        ### Create Session
        ipaddress, ipproxy = get_ipaddress(req)

        access_token, data_session = await UserAuthService().token_create(config_auth.JWT_SECRET_KEY, data_user, data_client.client_id, ipaddress)
        refresh_token = await UserAuthService().refresh_create(data_user, data_client.client_id, data_session.session_id)

        res = set_token_cookies(res, access_token)
        res = set_refresh_cookies(res, refresh_token)

        await ClientUserService().add_clientuser(data_client.id, data_user.username)
        await UserAuthService().generate_cache_user(data_user)
        await UserAuthService().generate_cache_menu(data_user)
        sleep(1)
