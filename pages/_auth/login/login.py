import os
from time import sleep
from typing import Annotated, Any
from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from core import PageResponse
from app._sys.user.service import UserQueryService
from app._sys.user.exceptions import UserNotFoundException, UserNotActiveException, PasswordDoesNotMatchException
from pages._auth.login.request import LoginRequest

router = APIRouter(prefix="/login")
page = PageResponse(os.path.dirname(__file__), router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_login(
    req: page_req,
    next: str = None,
):
    print("page[login]requser ", req.user)
    page.addContext("nextpage", next)
    return page.response("/html/login.html")


@router.get("/{PathCheck}/login.js")
async def page_js_login(next: str, req: page_req):
    if next is None or next == "None":
        next = "/page/dashboard"
    return page.response("/html/login.js")


@router.post("/{PathCheck}/login", status_code=201)
async def page_post_login(
    dataIn: LoginRequest,
    req: page_req,
):
    sleep(1)
    user_query = UserQueryService()
    data_get = await user_query.get_user_by(email=dataIn.email)
    if not data_get:
        raise UserNotFoundException
    if data_get.disabled:
        raise UserNotActiveException

    if not await user_query.verify_password(data_get, dataIn.password):
        raise PasswordDoesNotMatchException

    # user_cookie_token(response, user.username, user.list_scope, sess.id, sess.client_id, sess.session_id)
