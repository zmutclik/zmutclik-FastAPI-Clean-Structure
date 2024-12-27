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

    async def create_privilege(self, privilege: str, desc: str) -> PrivilegeSchema:
        if await self.privilege_repo.get(privilege):
            raise PrivilegeDuplicateException
        priv = Privilege.create(privilege=privilege, desc=desc)
        user = await self.privilege_repo.save(privilege=priv)
        return PrivilegeSchema.model_validate(user)

    async def update(self, privilege_id: int, privilege: Union[str, None], desc: Union[str, None]) -> PrivilegeSchema:
        privilege = await self.privilege_repo.get_by_id(privilege_id)
        if not user:
            raise PrivilegeNotFoundException
        if await self.privilege_repo.get(privilege):
            raise PrivilegeDuplicateException

        updates = {}
        if privilege:
            updates["privilege"] = privilege
        if desc:
            updates["desc"] = desc

        user = await self.privilege_repo.update(privilege, updates)
        return PrivilegeSchema.model_validate(privilege)
