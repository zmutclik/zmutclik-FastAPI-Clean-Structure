import os
from time import sleep
from typing import Annotated, Any
from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from core import PageResponse
from app._sys.user.service import UserQueryService
from app._sys.user.exceptions import UserNotFoundException, UserNotActiveException
from pages._auth.login.request import LoginRequest

login_router = APIRouter(prefix="/login")
page = PageResponse(os.path.dirname(__file__), login_router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@login_router.get("", response_class=HTMLResponse)
async def page_login(
    req: page_req,
    next: str = None,
):
    print("page[login]requser ", req.user)
    page.addContext("nextpage", next)
    return page.response("/html/login.html")


@login_router.get("/{PathCheck}/login.js")
async def page_js_login(next: str, req: page_req):
    if next is None or next == "None":
        next = "/page/dashboard"
    return page.response("/html/login.js")


@login_router.post("/{PathCheck}/login", status_code=201)
async def page_post_login(
    dataIn: LoginRequest,
    req: page_req,
):
    sleep(1)
    # userrepo = UsersRepository(db)

    # sess = SessionRepository().get(request.state.sessionId)
    # if sess is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Error.")
    # if sess.EndTime < datetime.now():
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session sudah Kadaluarsa.")
    user_query = UserQueryService()
    data_get = await user_query.get_user_by(email=dataIn.email)
    if not data_get:
        raise UserNotFoundException
    if data_get.disabled:
        raise UserNotActiveException
    
    # userreal = authenticate_user(user.username, dataIn.password, db)
    # if not userreal:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User atau Password anda Salah.!")

    # user_cookie_token(response, user.username, user.list_scope, sess.id, sess.client_id, sess.session_id)
