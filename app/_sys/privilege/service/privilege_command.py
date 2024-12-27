from typing import Union
from pythondi import inject

from app._sys.privilege.domain import Privilege
from app._sys.privilege.repository import PrivilegeRepo
from app._sys.privilege.schema import PrivilegeSchema
from app._sys.privilege.exceptions import PrivilegeNotFoundException, PrivilegeDuplicateException


class PrivilegeCommandService:
    @inject()
    def __init__(self, privilege_repo: PrivilegeRepo):
        self.privilege_repo = privilege_repo

    async def create(self, privilege: str, desc: str) -> PrivilegeSchema:
        if await self.privilege_repo.get(privilege):
            raise PrivilegeDuplicateException
        date_create = Privilege.create(privilege=privilege, desc=desc)
        data_saved = await self.privilege_repo.save(privilege=date_create)
        return PrivilegeSchema.model_validate(data_saved)

    async def update(self, privilege_id: int, privilege: Union[str, None], desc: Union[str, None]) -> PrivilegeSchema:
        data_get = await self.privilege_repo.get_by_id(privilege_id)
        if not data_get:
            raise PrivilegeNotFoundException
        if await self.privilege_repo.get(privilege):
            raise PrivilegeDuplicateException

        updates = {}
        if privilege:
            updates["privilege"] = privilege
        if desc:
            updates["desc"] = desc

        data_updated = await self.privilege_repo.update(data_get, updates)
        return data_updated
    
    async def delete(self, privilege_id: int,username:str) -> None:
        data_get = await self.privilege_repo.get_by_id(privilege_id)
        if not data_get:
            raise PrivilegeNotFoundException
        
        await self.privilege_repo.delete(data_get, username)
