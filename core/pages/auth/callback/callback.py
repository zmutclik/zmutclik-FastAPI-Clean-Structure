import os, httpx, jwt
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request
from core.config import config_auth
from core.pages.response import PageResponse
from ..logout.logout import page_auth_logout
from core.app.security.clientsso.service import ClientSSOService
from core.app.security.clientsso.exceptions import ClientSSONotFoundException
from core.exceptions import ForbiddenException, UnauthorizedException, BadRequestException
from core.fastapi.helper import get_ipaddress, set_refresh_cookies, set_token_cookies

router = APIRouter(prefix="/callback", tags=["AUTH / CALLBACK"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", status_code=200)
async def page_auth_callback(code: str, response: Response, request: Request):
    sso_token_url = config_auth.SSO_TOKEN_URL
    payload = {"grant_type": "authorization_code", "code": code, "client_id": config_auth.SSO_CLIENT_ID, "client_secret": config_auth.JWT_SECRET_KEY}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        try:
            sso_response = await client.post(sso_token_url, data=payload, headers=headers)
            sso_response.raise_for_status()  # Lempar error jika gagal
            token_data = sso_response.json()  # Ambil respons JSON
            try:
                payload = jwt.decode(
                    token_data["access_token"],
                    config_auth.JWT_SECRET_KEY,
                    algorithms=[config_auth.JWT_ALGORITHM],
                    options={"verify_exp": True},
                )
                user_roles = payload.get("roles", [])
                user_scopes = payload.get("permissions", [])
                user_username = payload.get("sub")
                user_session_id = payload.get("jti")

            except jwt.ExpiredSignatureError as e:
                raise UnauthorizedException
            except jwt.exceptions.PyJWTError:
                raise ForbiddenException

            response = set_token_cookies(response, token_data["access_token"], token_data["expires_in"])
            response = set_refresh_cookies(response, token_data["refresh_token"])

            response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
            response.headers["Location"] = f"/page/dashboard"
            return response

        except httpx.HTTPStatusError as e:
            return await page_auth_logout(response, request)
        except Exception as e:
            return await page_auth_logout(response, request)
