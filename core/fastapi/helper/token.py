from typing import Union
from datetime import timedelta, datetime, timezone

from fastapi import Request
from jose import JWTError, jwt
from core import config_auth
from jwt.exceptions import PyJWTError
from jwt import ExpiredSignatureError
from core.app.auth.user.schema import RefreshTokenSchema


def token_jwt(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config_auth.JWT_SECRET_KEY,
        algorithm=config_auth.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_refresh(request: Request) -> RefreshTokenSchema:
    refresh_token = request.cookies.get(config_auth.REFRESH_KEY)
    try:
        payload = jwt.decode(
            refresh_token,
            config_auth.JWT_SECRET_KEY,
            algorithms=[config_auth.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        refresh_token = RefreshTokenSchema(
            username=payload.get("sub"),
            session_id=payload.get("session"),
            client_id=payload.get("client"),
        )
    except PyJWTError:
        return False
    except ExpiredSignatureError:
        return False

    return refresh_token
