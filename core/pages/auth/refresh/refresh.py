import os
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request
from core.fastapi.helper import set_token_cookies, decode_refresh
from core.pages.response import PageResponse
from core.app.security.client.service import ClientService
from core.app.security.session.service import SessionService
import jwt
from core.fastapi.helper import get_ipaddress
from core.app.auth.user.service import UserQueryService, UserAuthService
from ..logout.logout import page_auth_logout

router = APIRouter(prefix="/refresh", tags=["AUTH / REFRESH"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.api_route("", status_code=201, methods=["GET", "POST"])
async def page_auth_refresh(backRouter: str, response: Response, request: page_req):
    #### Cek Client ID
    data_client = await ClientService().get_client_id(request.user.client_id)
    if data_client is None:
        return page_auth_logout(response, request)
    if data_client.disabled:
        return page_auth_logout(response, request)

    refresh_token = decode_refresh(request)

    ipaddress, ipproxy = get_ipaddress(request)

    data_client = await ClientService().update_clientuser(
        client_id=data_client.id,
        user=refresh_token.username,
        LastPage=backRouter,
        Lastipaddress=ipaddress,
    )
    if data_client is None:
        return page_auth_logout(response, request)

    data_session = await SessionService().update_session(refresh_token.session_id, LastPage=backRouter, Lastipaddress=ipaddress)
    if data_session is None:
        return page_auth_logout(response, request)

    data_user = await UserQueryService().get_user_by(username=refresh_token.username)
    access_token, data_session = await UserAuthService().token_create(data_user, refresh_token.client_id, ipaddress, data_session)

    response = set_token_cookies(response, access_token)

    if request.method == "GET":
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    elif request.method == "POST":
        response.status_code = 307  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = backRouter
    return response
