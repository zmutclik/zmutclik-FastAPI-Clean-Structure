from typing import Union
from pythondi import inject

from ..domain import MenuType
from ..repository import MenuTypeRepo
from ..schema import MenuTypeSchema
from ..exceptions import MenuTypeNotFoundException, MenuTypeDuplicateException


class MenuTypeCommandService:
    @inject()
    def __init__(self, menutype_repo: MenuTypeRepo):
        self.menutype_repo = menutype_repo

    async def create_menutype(self, menutype: str, desc: str) -> MenuTypeSchema:
        if await self.menutype_repo.get_menutype_by(menutype):
            raise MenuTypeDuplicateException
        data_create = MenuType.create(menutype=menutype, desc=desc)
        data_saved = await self.menutype_repo.save_menutype(menutype=data_create)
        return data_saved

    async def update_menutype(self, menutype_id: int, menutype: Union[str, None], desc: Union[str, None]) -> MenuTypeSchema:
        data_get = await self.menutype_repo.get_menutype(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException
        if await self.menutype_repo.get_menutype_by(menutype):
            raise MenuTypeDuplicateException

        updates = {}
        if menutype:
            updates["menutype"] = menutype
        if desc:
            updates["desc"] = desc

        data_updated = await self.menutype_repo.update_menutype(data_get, updates)
        return data_updated

    async def delete_menutype(self, menutype_id: int, username: str) -> None:
        data_get = await self.menutype_repo.get_menutype(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException

        await self.menutype_repo.delete_menutype(data_get, username)
