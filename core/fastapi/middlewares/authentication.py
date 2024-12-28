from typing import Optional, Tuple
from datetime import datetime, timezone
import jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config
from ..schemas import CurrentUser


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
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
            user_id = payload.get("sub")
            user_role = payload.get("role")
            user_scopes = payload.get("scopes", [])
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.id = user_id
        current_user.role = user_role
        current_user.scopes = user_scopes
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
