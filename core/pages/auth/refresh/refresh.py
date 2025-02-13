import os, httpx, jwt
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request
from core.fastapi.helper import set_token_cookies, decode_refresh
from core.pages.response import PageResponse
from core.app.security.client.service import ClientService, ClientUserService
from core.app.security.session.service import SessionService
import jwt
from core.fastapi.helper import get_ipaddress
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.exceptions import ForbiddenException, UnauthorizedException, BadRequestException
from ..logout.logout import page_auth_logout
from core import config_auth

router = APIRouter(prefix="/refresh", tags=["AUTH / REFRESH"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


async def page_auth_refresh(redirect_uri: str, response: Response, request: Request):
    sso_token_url = config_auth.SSO_TOKEN_URL
    credentials = request.cookies.get(config_auth.REFRESH_KEY)

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": credentials,
        "client_id": config_auth.SSO_CLIENT_ID,
        "client_secret": config_auth.JWT_SECRET_KEY,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        try:
            sso_response = await client.post(sso_token_url, data=payload, headers=headers)
            sso_response.raise_for_status()  # Lempar error jika gagal
            token_data = sso_response.json()  # Ambil respons JSON
            try:
                payload = jwt.decode(
                    token_data["access_token"], config_auth.JWT_SECRET_KEY, algorithms=[config_auth.JWT_ALGORITHM], options={"verify_exp": True}
                )
                user_roles = payload.get("roles", [])
                user_scopes = payload.get("permissions", [])
                user_username = payload.get("sub")
                user_session_id = payload.get("jti")

            except jwt.ExpiredSignatureError:
                raise UnauthorizedException("Token expired")
            except jwt.exceptions.PyJWTError:
                raise ForbiddenException("Token invalid")

            access_token = token_data["access_token"]

        except httpx.HTTPStatusError as e:
            return await page_auth_logout(response, request)
        except Exception as e:
            return await page_auth_logout(response, request)

        # ipaddress, ipproxy = get_ipaddress(request)
        # await ClientUserService().update_clientuser(
        #     client_id=request.user.client_id,
        #     user=user_username,
        #     LastPage=redirect_uri,
        #     Lastipaddress=ipaddress,
        # )
        # await SessionService().update_session(user_session_id, Lastipaddress=ipaddress)

    response = set_token_cookies(response, access_token)
    if request.method == "GET":
        response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    elif request.method == "POST":
        response.status_code = 307  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = redirect_uri
    return response


@router.get("")
async def page_auth_refresh_get(redirect_uri: str, response: Response, request: Request):
    return await page_auth_refresh(redirect_uri, response, request)


@router.post("")
async def page_auth_refresh_post(redirect_uri: str, response: Response, request: Request):
    return await page_auth_refresh(redirect_uri, response, request)
