import os, json, urllib.parse
from time import sleep
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Response, Depends, Request, Form
from pydantic import ValidationError
from core.config import config_auth
from core.fastapi.helper import get_ipaddress, set_refresh_cookies, set_token_cookies, decode_refresh
from core.app.auth.user.service import UserQueryService, UserAuthService
from core.app.security.client.service import ClientService, ClientUserService
from core.app.security.client.exceptions import ClientNotFoundException
from core.app.security.clientsso.service import ClientSSOService
from core.app.security.clientsso.exceptions import ClientSSONotFoundException
from core.app.security.session.service import SessionService
from core.exceptions import ForbiddenException, UnauthorizedException
from core.pages.response import PageResponse
from .request import TokenRequest
from .response import TokenResponse

router = APIRouter(prefix="/token", tags=["AUTH / TOKEN"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


async def get_form_data(grant_type: str = Form(...), client_id: str = Form(...), client_secret: str = Form(...), code: str = Form(...)):
    return {"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret, "code": code}


async def validate_authcode(data_dict: dict):
    try:
        data_validated = TokenRequest.model_validate(data_dict)
        return data_validated
    except ValidationError as e:
        raise UnauthorizedException


@router.post(
    "",
    status_code=201,
    response_model=TokenResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "grant_type": {"type": "string", "description": "Tipe grant (contoh: authorization_code)"},
                            "client_id": {"type": "string", "description": "ID unik client"},
                            "client_secret": {"type": "string", "description": "Secret key untuk autentikasi"},
                            "code": {"type": "string", "description": "Kode otorisasi"},
                        },
                        "required": ["grant_type", "client_id", "client_secret", "code"],
                    }
                }
            }
        }
    },
)
async def page_auth_token(response: Response, request: Request):
    """
    Endpoint untuk menerima token dari JSON atau Form-Data.

    **Input bisa dalam format:**
    - **JSON (`application/json`)**
    - **Form (`application/x-www-form-urlencoded`)**

    **Kedua format memiliki parameter yang sama:**
    - `grant_type`: Tipe grant (contoh: `authorization_code`)
    - `client_id`: ID unik client
    - `client_secret`: Secret key untuk autentikasi
    - `code`: Kode otorisasi yang diberikan oleh server otentikasi (SSO)

    **Respon:**
    - Jika request valid, akan mengembalikan data yang dikirim beserta sumbernya (`json` atau `form`).
    - Jika request tidak valid, akan mengembalikan error 400 atau 401.
    """
    body_bytes = await request.body()
    ipaddress, ipproxy = get_ipaddress(request)
    if not body_bytes:
        raise ForbiddenException

    try:
        json_data = await request.json()
        data_validated = await validate_authcode(json_data)
    except json.JSONDecodeError:
        body = await request.body()
        decoded_body = body.decode("utf-8")
        parsed_data = dict(urllib.parse.parse_qsl(decoded_body))
        data_validated = await validate_authcode(parsed_data)

    ###################################################################################################################
    if data_validated.client_id == config_auth.SSO_CLIENT_ID:
        clientsso_id = config_auth.SSO_CLIENT_ID
        clientsso_secret = config_auth.JWT_SECRET_KEY
    else:
        data_clientsso = await ClientSSOService().get_clientsso(data_validated.client_id)
        if data_clientsso is None:
            raise ClientSSONotFoundException
        if data_clientsso.ipaddress != ipaddress:
            raise ForbiddenException
        clientsso_id = data_validated.client_id
        clientsso_secret = data_clientsso.clientsso_secret

    ###################################################################################################################
    if data_validated.grant_type == "refresh_token":
        if data_validated.refresh_token is None:
            raise UnauthorizedException

        refresh_token = data_validated.refresh_token
        refresh_decoded = decode_refresh(clientsso_secret, data_validated.refresh_token)
        if not refresh_decoded:
            raise UnauthorizedException

        data_client = await ClientService().get_client_id(refresh_decoded.client_id)
        if data_client is None:
            raise UnauthorizedException
        if data_client.disabled:
            raise UnauthorizedException

        data_clientuser = await ClientUserService().get_clientuser(data_client.id, refresh_decoded.username)
        if data_clientuser is None:
            raise UnauthorizedException

        await ClientUserService().update_clientuser(client_id=data_client.id, user=refresh_decoded.username, LastPage="", Lastipaddress="")

        data_session = await SessionService().update_session(refresh_decoded.session_id)
        if not data_session:
            raise UnauthorizedException

        data_user = await UserQueryService().get_user_by(username=refresh_decoded.username)
        access_token = await UserAuthService().token_create(clientsso_secret, data_user, refresh_decoded.client_id)

    elif data_validated.grant_type == "authorization_code":
        if data_validated.code is None:
            raise UnauthorizedException

        data_clientsso_code = await ClientSSOService().get_clientsso_code(clientsso_id, data_validated.code)
        if data_clientsso_code is None:
            print("Code not found")
            raise UnauthorizedException
        await ClientSSOService().delete_clientsso_code(data_clientsso_code.client_id)

        data_client = await ClientService().get_client_id(data_clientsso_code.client_id)
        if data_client is None:
            print("Client not found")
            raise UnauthorizedException
        if data_client.disabled:
            raise UnauthorizedException

        data_user = await UserQueryService().get_user(data_clientsso_code.user_id)
        await ClientUserService().add_clientuser(data_client.id, data_user.username)
        session_end = datetime.now(timezone.utc) + timedelta(minutes=config_auth.REFRESH_EXPIRED)
        data_session = await SessionService().create_session(
            client_id=data_clientsso_code.client_id,
            user=data_user.username,
            session_end=session_end,
            ipaddress=ipaddress,
        )
        ### Create Session
        access_token = await UserAuthService().token_create(clientsso_secret, data_user, data_session.client_id)
        refresh_token = await UserAuthService().refresh_create(data_user, data_clientsso_code.client_id, data_session.session_id)

    else:
        raise ForbiddenException

    return TokenResponse(
        access_token=access_token,
        expires_in=config_auth.COOKIES_EXPIRED * 60,
        refresh_token=refresh_token,
        id_token=data_session.session_id,
    )
