from typing import Union, Optional
from pythondi import inject

from ..domain import AuthConfig
from ..repository import AuthConfigRepo
from ..schema import AuthConfigSchema


class AuthConfigService:
    @inject()
    def __init__(self, authconfig_repo: AuthConfigRepo):
        self.authconfig_repo = authconfig_repo

    async def get_authconfig(self) -> Optional[AuthConfigSchema]:
        return await self.authconfig_repo.get()

    async def update_authconfig(self, dataIn: AuthConfigSchema) -> AuthConfigSchema:
        data_get = await self.authconfig_repo.get()

        updates = {}
        if data_get.jwt_scret_key != dataIn.jwt_scret_key:
            updates["jwt_scret_key"] = dataIn.jwt_scret_key
        if data_get.jwt_algorithm != dataIn.jwt_algorithm:
            updates["jwt_algorithm"] = dataIn.jwt_algorithm
        if data_get.cookies_prefix != dataIn.cookies_prefix:
            updates["cookies_prefix"] = dataIn.cookies_prefix
        if data_get.cookies_https != dataIn.cookies_https:
            updates["cookies_https"] = dataIn.cookies_https
        if data_get.cookies_exp != dataIn.cookies_exp:
            updates["cookies_exp"] = dataIn.cookies_exp
        if data_get.refresh_exp != dataIn.refresh_exp:
            updates["refresh_exp"] = dataIn.refresh_exp
        if data_get.timeout_exp != dataIn.timeout_exp:
            updates["timeout_exp"] = dataIn.timeout_exp
        if data_get.sso_login_url != dataIn.sso_login_url:
            updates["sso_login_url"] = dataIn.sso_login_url
        if data_get.sso_token_url != dataIn.sso_token_url:
            updates["sso_token_url"] = dataIn.sso_token_url
        if data_get.sso_client_id != dataIn.sso_client_id:
            updates["sso_client_id"] = dataIn.sso_client_id
        if data_get.register_account != dataIn.register_account:
            updates["register_account"] = dataIn.register_account
        if data_get.login_by_otp != dataIn.login_by_otp:
            updates["login_by_otp"] = dataIn.login_by_otp

        data_updated = await self.authconfig_repo.update(data_get, **updates)
        return data_updated
