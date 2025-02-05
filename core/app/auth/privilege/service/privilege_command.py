from typing import Union
from pythondi import inject

from core.exceptions import NotFoundException, DuplicateValueException
from ..domain import Privilege, PrivilegeMenus
from ..repository import PrivilegeRepo, PrivilegeMenusRepo
from ..schema import PrivilegeSchema


class PrivilegeCommandService:
    @inject()
    def __init__(self, privilege_repo: PrivilegeRepo, privilege_menu_repo: PrivilegeMenusRepo):
        self.privilege_repo = privilege_repo
        self.privilege_menu_repo = privilege_menu_repo

    async def create_privilege(self, created_user: str, privilege: str, desc: str, menutype_id: int, menus: list[int] = [1]) -> PrivilegeSchema:
        if await self.privilege_repo.get_privilege_by(privilege):
            raise DuplicateValueException("Privilege already exists")
        
        date_create = Privilege.create(created_user=created_user, privilege=privilege, desc=desc)
        data_saved = await self.privilege_repo.save_privilege(privilege=date_create)

        for item in menus:
            privilege_menu = PrivilegeMenus.create(data_saved.id, menutype_id, item)
            await self.privilege_menu_repo.save_privilege_menu(privilege_menu=privilege_menu)

        return data_saved

    async def update_privilege(
        self,
        privilege_id: int,
        privilege: Union[str, None],
        desc: Union[str, None],
        menutype_id: Union[int, None],
        menus: list[int] = [],
    ) -> PrivilegeSchema:
        data_get = await self.privilege_repo.get_privilege(privilege_id)
        if not data_get:
            raise NotFoundException("Privilege not found")

        updates = {}
        if privilege is not None and privilege != data_get.privilege:
            updates["privilege"] = privilege
        if desc is not None and desc != data_get.desc:
            updates["desc"] = desc

        data_updated = await self.privilege_repo.update_privilege(data_get, **updates)

        await self.privilege_menu_repo.delete_privilege_menus(privilege_id=privilege_id, menutype_id=menutype_id)
        for item in menus:
            privilege_menu = PrivilegeMenus.create(privilege_id, menutype_id, item)
            await self.privilege_menu_repo.save_privilege_menu(privilege_menu=privilege_menu)

        return data_updated

    async def delete_privilege(self, privilege_id: int, username: str) -> None:
        data_get = await self.privilege_repo.get_privilege(privilege_id)
        if not data_get:
            raise NotFoundException("Privilege not found")

        await self.privilege_repo.delete_privilege(data_get, username)
