from typing import Union, Optional
from pythondi import inject

from ..domain import CoreSYSTEM
from ..repository import CoreSYSTEMRepo
from ..schema import CoreSYSTEMSchema


class CoreSYSTEMService:
    @inject()
    def __init__(self, coresystem_repo: CoreSYSTEMRepo):
        self.coresystem_repo = coresystem_repo

    async def get_coresystem(self) -> Optional[CoreSYSTEMSchema]:
        return await self.coresystem_repo.get()

    async def update_coresystem(self, dataIn: CoreSYSTEMSchema) -> CoreSYSTEMSchema:
        data_get = await self.coresystem_repo.get()

        updates = {}
        if data_get.environment != dataIn.environment:
            updates["environment"] = dataIn.environment
        if data_get.app_name != dataIn.app_name:
            updates["app_name"] = dataIn.app_name
        if data_get.app_desc != dataIn.app_desc:
            updates["app_desc"] = dataIn.app_desc
        if data_get.app_host != dataIn.app_host:
            updates["app_host"] = dataIn.app_host
        if data_get.app_port != dataIn.app_port:
            updates["app_port"] = dataIn.app_port
        if data_get.client_key != dataIn.client_key:
            updates["client_key"] = dataIn.client_key
        if data_get.jwt_scret_key != dataIn.jwt_scret_key:
            updates["jwt_scret_key"] = dataIn.jwt_scret_key
        if data_get.jwt_algorithm != dataIn.jwt_algorithm:
            updates["jwt_algorithm"] = dataIn.jwt_algorithm
        if data_get.cookies_key != dataIn.cookies_key:
            updates["cookies_key"] = dataIn.cookies_key
        if data_get.cookies_exp != dataIn.cookies_exp:
            updates["cookies_exp"] = dataIn.cookies_exp
        if data_get.debug != dataIn.debug:
            updates["debug"] = dataIn.debug

        data_updated = await self.coresystem_repo.update(data_get, **updates)
        return data_updated
