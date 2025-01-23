from typing import Optional, Tuple
from datetime import datetime, timezone
import jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from http.cookies import SimpleCookie

from core import config
from ..schemas import CurrentUser


def get_specific_cookie(connection: HTTPConnection, cookie_name: str) -> str:
    cookie_header = connection.headers.get("cookie", "")
    cookies = dict(item.split("=", 1) for item in cookie_header.split("; ") if "=" in item)
    return cookies.get(cookie_name)


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        authorization_cookie: str = get_specific_cookie(conn, config.COOKIES_KEY)
        current_user.client_id = get_specific_cookie(conn, config.CLIENT_KEY)

        if "api" in conn.scope["path"] and "api." not in conn.scope["path"]:
            current_user.channel = "api"
        if "page" in conn.scope["path"] or "auth/tim" in conn.scope["path"] or "auth/log" in conn.scope["path"] or "auth/reg" in conn.scope["path"]:
            current_user.channel = "page"
        if "static" in conn.scope["path"] or "favicon" in conn.scope["path"] or "openapi.json" in conn.scope["path"]:
            current_user.channel = "static"
        if "page" in conn.scope["path"] and ".js" in conn.scope["path"]:
            current_user.channel = "page_js"

        if authorization is not None:
            try:
                scheme, credentials = authorization.split(" ")
                if scheme.lower() != "bearer":
                    return False, current_user
            except ValueError:
                return False, current_user
        elif authorization_cookie is not None and current_user.channel != "api":
            credentials = authorization_cookie
        else:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
                options={"verify_exp": True},
            )
            user_roles = payload.get("roles", [])
            user_scopes = payload.get("permissions", [])
            user_username = payload.get("sub")
            user_session_id = payload.get("jti")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.roles = user_roles
        current_user.scopes = user_scopes
        current_user.username = user_username
        current_user.session_id = user_session_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
