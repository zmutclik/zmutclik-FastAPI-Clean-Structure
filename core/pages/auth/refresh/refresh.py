import os
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request
from core.config import config_auth
from fastapi.responses import RedirectResponse
from core.pages.response import PageResponse
from core.app.security.client.service import ClientService
from core.app.security.session.service import SessionService
import jwt
from core.app.auth.user.service import UserQueryService, UserAuthService

router = APIRouter(prefix="/refresh", tags=["AUTH / REFRESH"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


def redirect_to_login(response: Response):
    response.delete_cookie(key=config_auth.COOKIES_KEY)
    response.delete_cookie(key=config_auth.REFRESH_KEY)
    response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = f"/auth/login"
    return response


@router.api_route("", status_code=201, methods=["GET", "POST"])
async def page_auth_refresh(backRouter: str, response: Response, request: page_req):
    refresh_token = request.cookies.get(config_auth.REFRESH_KEY)
    try:
        payload = jwt.decode(
            refresh_token,
            config_auth.JWT_SECRET_KEY,
            algorithms=[config_auth.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        user_username = payload.get("sub")
        user_session_id = payload.get("session")
        user_client_id = payload.get("client")
    except jwt.exceptions.PyJWTError:
        return redirect_to_login(response)
    except jwt.ExpiredSignatureError:
        return redirect_to_login(response)

    ipaddress = request.client.host
    try:
        if request.headers.get("X-Real-IP") is not None:
            ipaddress = request.headers.get("X-Real-IP")
    except:
        pass

    data_client = await ClientService().get_client_id(user_client_id)
    data_session = await SessionService().get_session_id(user_session_id)
    if data_client is None or data_session is None:
        return redirect_to_login(response)
    if not await ClientService().update_clientuser(client_id=data_client.id, LastLogin=datetime.now(timezone.utc), user=user_username, LastPage=backRouter, Lastipaddress=ipaddress):
        return redirect_to_login(response)
    await SessionService().update_session(data_session.id, datetime.now(timezone.utc), LastPage=backRouter, Lastipaddress=ipaddress)

    data_get = await UserQueryService().get_user_by(username=user_username)
    access_token, session_id = await UserAuthService().token_create(data_get, user_client_id, ipaddress, user_session_id)
    access_token_time = datetime.now(timezone.utc) + timedelta(minutes=config_auth.COOKIES_EXPIRED)
    access_token_str = access_token_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        key=config_auth.COOKIES_KEY,
        value=access_token,
        httponly=True,
        expires=access_token_str,
    )

    if request.method == "GET":
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    elif request.method == "POST":
        response.status_code = 307  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = backRouter
    return response
