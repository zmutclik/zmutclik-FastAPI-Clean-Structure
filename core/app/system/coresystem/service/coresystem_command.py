from typing import Union 
from pythondi import inject 
 
from app.coresystem.domain import CoreSYSTEM 
from app.coresystem.repository import CoreSYSTEMRepo 
from app.coresystem.schema import CoreSYSTEMSchema 
from app.coresystem.exceptions import CoreSYSTEMNotFoundException, CoreSYSTEMDuplicateException 
 
 
class CoreSYSTEMCommandService: 
    @inject() 
    def __init__(self, coresystem_repo: CoreSYSTEMRepo): 
        self.coresystem_repo = coresystem_repo 
 
    async def create_coresystem(self, coresystem: str) -> CoreSYSTEMSchema: 
        if await self.coresystem_repo.get(coresystem): 
            raise CoreSYSTEMDuplicateException 
        data_create = CoreSYSTEM.create(coresystem=coresystem) 
        data_saved = await self.coresystem_repo.save(coresystem=data_create) 
        return data_saved 
 
    async def update_coresystem(self, coresystem_id: int, coresystem: Union[str, None]) -> CoreSYSTEMSchema: 
        data_get = await self.coresystem_repo.get_by_id(coresystem_id) 
        if not data_get: 
            raise CoreSYSTEMNotFoundException 
        if await self.coresystem_repo.get(coresystem): 
            raise CoreSYSTEMDuplicateException 
 
        updates = {} 
        if coresystem: 
            updates["coresystem"] = coresystem 
 
        data_updated = await self.coresystem_repo.update(data_get, updates) 
        return data_updated 
 
    async def delete_coresystem(self, coresystem_id: int, username: str) -> None: 
        data_get = await self.coresystem_repo.get_by_id(coresystem_id) 
        if not data_get: 
            raise CoreSYSTEMNotFoundException 
 
        await self.coresystem_repo.delete(data_get, username) 
