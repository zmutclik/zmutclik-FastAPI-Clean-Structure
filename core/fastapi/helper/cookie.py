from datetime import datetime, timedelta, timezone
from fastapi import Response
from core import config_auth


def set_token_cookies(response: Response, access_token: str, max_age: int = 0) -> Response:
    if max_age == 0:
        max_age = config_auth.COOKIES_EXPIRED * 60

    response.set_cookie(
        key=config_auth.COOKIES_KEY,
        value=access_token,
        httponly=True,
        max_age=max_age,
        secure=config_auth.COOKIES_HTTPS,
    )
    return response


def set_refresh_cookies(response: Response, refresh_token: str) -> Response:
    token_time = datetime.now(timezone.utc) + timedelta(minutes=config_auth.REFRESH_EXPIRED)
    token_time_str = token_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        key=config_auth.REFRESH_KEY,
        value=refresh_token,
        httponly=True,
        expires=token_time_str,
        secure=config_auth.COOKIES_HTTPS,
    )
    return response
