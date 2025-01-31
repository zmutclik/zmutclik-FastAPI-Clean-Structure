import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request
from core.config import config
from fastapi.responses import RedirectResponse
from core.pages.response import PageResponse
import jwt
from core.app.auth.user.service import UserQueryService, UserAuthService

router = APIRouter(prefix="/refresh", tags=["AUTH / REFRESH"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.api_route("", status_code=201, methods=["GET", "POST"])
async def page_auth_refresh(backRouter: str, response: Response, request: page_req):
    refresh_token = request.cookies.get(config.REFRESH_KEY)
    try:
        payload = jwt.decode(
            refresh_token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        user_username = payload.get("sub")
        user_session_id = payload.get("session")
        user_client_id = payload.get("client")
    except jwt.exceptions.PyJWTError:
        response.delete_cookie(key=config.COOKIES_KEY)
        response.delete_cookie(key=config.REFRESH_KEY)
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
        response.headers["Location"] = f"/auth/login"
        return response
    except jwt.ExpiredSignatureError:
        response.delete_cookie(key=config.COOKIES_KEY)
        response.delete_cookie(key=config.REFRESH_KEY)
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
        response.headers["Location"] = f"/auth/login"
        return response

    data_get = await UserQueryService().get_user_by(username=user_username)
    access_token = await UserAuthService().token_create(data_get)
    access_token_time = datetime.now(timezone.utc) + timedelta(minutes=config.COOKIES_EXPIRED)
    access_token_str = access_token_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key=config.COOKIES_KEY, value=access_token, httponly=True, expires=access_token_str)

    if request.method == "GET":
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    elif request.method == "POST":
        response.status_code = 307  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = backRouter
    return response
