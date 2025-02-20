from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AuthConfigSchema(BaseModel):
    sso_login_url: str
    sso_token_url: str
    sso_client_id: str
    jwt_scret_key: str
    jwt_algorithm: str
    cookies_prefix: str
    cookies_https: bool
    cookies_exp: int
    refresh_exp: int
    timeout_exp: int
    register_account: bool
