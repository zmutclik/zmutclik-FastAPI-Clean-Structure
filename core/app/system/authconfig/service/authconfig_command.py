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

        data_updated = await self.authconfig_repo.update(data_get, **updates)
        return data_updated
