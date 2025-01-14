from typing import Union
from pythondi import inject

from ..domain import Privilege
from ..repository import PrivilegeRepo
from ..schema import PrivilegeSchema
from ..exceptions import PrivilegeNotFoundException, PrivilegeDuplicateException


class PrivilegeCommandService:
    @inject()
    def __init__(self, privilege_repo: PrivilegeRepo):
        self.privilege_repo = privilege_repo

    async def create_privilege(self, privilege: str, desc: str) -> PrivilegeSchema:
        if await self.privilege_repo.get_privilege_by(privilege):
            raise PrivilegeDuplicateException
        date_create = Privilege.create(privilege=privilege, desc=desc)
        data_saved = await self.privilege_repo.save_privilege(privilege=date_create)
        return data_saved

    async def update_privilege(self, privilege_id: int, privilege: Union[str, None], desc: Union[str, None]) -> PrivilegeSchema:
        data_get = await self.privilege_repo.get_privilege(privilege_id)
        if not data_get:
            raise PrivilegeNotFoundException
        if await self.privilege_repo.get_privilege_by(privilege):
            raise PrivilegeDuplicateException

        updates = {}
        if privilege:
            updates["privilege"] = privilege
        if desc:
            updates["desc"] = desc

        data_updated = await self.privilege_repo.update_privilege(data_get, updates)
        return data_updated
    
    async def delete_privilege(self, privilege_id: int,username:str) -> None:
        data_get = await self.privilege_repo.get_privilege(privilege_id)
        if not data_get:
            raise PrivilegeNotFoundException
        
        await self.privilege_repo.delete_privilege(data_get, username)
