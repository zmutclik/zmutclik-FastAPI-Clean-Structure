import os
from time import sleep
from typing import Annotated, Any
from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from core import config
from core.pages.response import PageResponse
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.auth.user.exceptions import UserNotFoundException, UserNotActiveException, PasswordDoesNotMatchException
from core.pages.auth.login.request import LoginRequest

router = APIRouter(prefix="/login")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_login(
    req: page_req,
    next: str = None,
):
    page.addContext("nextpage", next)
    return page.response(req, "/html/login.html")


@router.get("/{PathCheck}.js")
async def page_js_login(next: str, req: page_req):
    if next is None or next == "None":
        next = "/page/dashboard"
    page.addContext("nextpage", next)
    return page.response(req, "/html/login.js")


@router.post("/{PathCheck}", status_code=201)
async def page_post_login(dataIn: LoginRequest, req: page_req, res: Response):
    user_query = UserQueryService()
    data_get = await user_query.get_user_by(email=dataIn.email)
    if not data_get:
        raise UserNotFoundException
    if data_get.disabled:
        raise UserNotActiveException

    if not await user_query.verify_password(data_get, dataIn.password):
        raise PasswordDoesNotMatchException

    access_token = await UserAuthService().token_create(data_get)
    res.set_cookie(key=config.COOKIES_KEY, value=access_token)
    
    await UserAuthService().generate_cache_user(data_get)
    await UserAuthService().generate_cache_menu(data_get)
    # sleep(1)
