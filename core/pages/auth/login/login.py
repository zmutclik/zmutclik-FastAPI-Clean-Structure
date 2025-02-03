import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from core import config_auth
from core.pages.response import PageResponse
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.security.client.service import ClientService
from core.app.auth.user.exceptions import UserNotFoundException, UserNotActiveException, PasswordDoesNotMatchException
from core.pages.auth.login.request import LoginRequest

router = APIRouter(prefix="/login")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_auth_login(
    req: page_req,
    next: str = None,
):
    page.addContext("nextpage", next)
    return page.response(req, "/html/login.html")


@router.get("/{PathCheck}.js")
async def page_auth_login_js(next: str, req: page_req):
    if next is None or next == "None":
        next = "/page/dashboard"
    page.addContext("nextpage", next)
    return page.response(req, "/html/login.js")


@router.post("/{PathCheck}", status_code=201)
async def page_auth_login_sign(dataIn: LoginRequest, req: page_req, res: Response):  #
    data_get = await UserQueryService().get_user_by(email=dataIn.email)
    if not data_get:
        raise UserNotFoundException
    if data_get.disabled:
        raise UserNotActiveException

    if not await UserQueryService().verify_password(data_get, dataIn.password):
        raise PasswordDoesNotMatchException

    access_token = await UserAuthService().token_create(data_get)
    refresh_token = await UserAuthService().refresh_create(data_get, req.user.client_id, req.user.session_id)

    access_token_time = datetime.now(timezone.utc) + timedelta(minutes=config_auth.COOKIES_EXPIRED)
    access_token_str = access_token_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    refresh_token_time = datetime.now(timezone.utc) + timedelta(minutes=config_auth.REFRESH_EXPIRED)
    refresh_token_str = refresh_token_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    res.set_cookie(key=config_auth.COOKIES_KEY, value=access_token, httponly=True, expires=access_token_str)
    res.set_cookie(key=config_auth.REFRESH_KEY, value=refresh_token, httponly=True, expires=refresh_token_str)

    await UserAuthService().generate_cache_user(data_get)
    await UserAuthService().generate_cache_menu(data_get)

    print("client_id = ", req.user.client_id)
    print("username = ", data_get.username)
    await ClientService().add_user(req.user.client_id, data_get.username)

    sleep(1)
