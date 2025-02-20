import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import APIRouter, Response, Depends
from fastapi.responses import HTMLResponse
from core import config_auth, config
from core.fastapi.helper import get_ipaddress, set_refresh_cookies, set_token_cookies
from core.pages.response import PageResponse
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.auth.user.exceptions import UserNotFoundException
from core.app.security.client.service import ClientService, ClientUserService
from core.app.security.client.exceptions import ClientNotFoundException
from core.app.security.clientsso.service import ClientSSOService
from core.app.security.clientsso.exceptions import ClientSSONotFoundException
from core.app.security.session.service import SessionService
from fastapi.exceptions import RequestValidationError
from core.pages.auth.login.request import LoginRequest
from ..logout.logout import page_auth_logout

router = APIRouter(prefix="/login")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_auth_login(req: page_req, res: Response, redirect_uri: str = None, client_id: str = None):
    title_form = config.APP_NAME
    if client_id is not None:
        data_clientsso = await ClientSSOService().get_clientsso(client_id)
        if data_clientsso is None or redirect_uri is None:
            return await page_auth_logout(res, req)
        if data_clientsso.callback_uri != redirect_uri:
            return await page_auth_logout(res, req)
        title_form = data_clientsso.nama
    else:
        client_id = "-"

    if redirect_uri is None or redirect_uri == "None":
        redirect_uri = "/page/dashboard"

    page.addContext("redirect_uri", redirect_uri)
    page.addContext("clientsso_id", client_id)
    page.addContext("title_form", title_form)
    page.addContext("register_account", config_auth.REGISTER_ACCOUNT)
    return page.response(req, "/html/login.html")


@router.get("/{PathCheck}.js")
async def page_auth_login_js(req: page_req, client_id: str = None):
    if client_id is None or client_id == "None":
        client_id = "-"
    page.addContext("clientsso_id", client_id)
    return page.response(req, "/html/login.js")


@router.get("/clear/client_id")
async def page_auth_clear_client_id(response: Response, request: page_req):
    response.delete_cookie(key=config_auth.CLIENT_KEY)
    response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = f"/auth/login"
    return response


@router.post("/{PathCheck}", status_code=201)
async def page_auth_login_sign(dataIn: LoginRequest, req: page_req, res: Response):  #
    #### Cek Client ID
    data_client = await ClientService().get_client_id(req.user.client_id)
    if data_client is None:
        raise ClientNotFoundException
    if data_client.disabled:
        errors = [
            {"loc": ["body", "email"], "msg": f'client "{data_client.client_id}" di disable', "type": ""},
            {"loc": ["body", "password"], "msg": f'client "{data_client.client_id}" di disable', "type": ""},
        ]
        raise RequestValidationError(errors)

    #### Cek User
    data_user = await UserQueryService().get_user_by(email=dataIn.email)
    if not data_user:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"email {dataIn.email} tidak terdaftar", "type": ""}])
    if data_user.disabled:
        raise RequestValidationError([{"loc": ["body", "email"], "msg": f"akun telah di disabled", "type": ""}])

    verify_password = await UserQueryService().verify_password(data_user, dataIn.password)
    if not verify_password:
        raise RequestValidationError([{"loc": ["body", "password"], "msg": f"password tidak sama", "type": ""}])

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

    # else:
    #     ### Create Session
    #     ipaddress, ipproxy = get_ipaddress(req)
    #     session_end = datetime.now(timezone.utc) + timedelta(minutes=config_auth.REFRESH_EXPIRED)
    #     data_session = await SessionService().create_session(
    #         client_id=data_client.client_id,
    #         user=data_user.username,
    #         session_end=session_end,
    #         ipaddress=ipaddress,
    #     )
    #     access_token = await UserAuthService().token_create(config_auth.JWT_SECRET_KEY, data_user, data_client.client_id, ipaddress)
    #     refresh_token = await UserAuthService().refresh_create(data_user, data_client.client_id, data_session.session_id)

    #     res = set_token_cookies(res, access_token)
    #     res = set_refresh_cookies(res, refresh_token)

    #     await ClientUserService().add_clientuser(data_client.id, data_user.username)
    #     await UserAuthService().generate_cache_user(data_user)
    #     await UserAuthService().generate_cache_menu(data_user)
    #     sleep(1)
