from typing import Union
from pythondi import inject

from app._sys.menutype.domain import MenuType
from app._sys.menutype.repository import MenuTypeRepo
from app._sys.menutype.schema import MenuTypeSchema
from app._sys.menutype.exceptions import MenuTypeNotFoundException, MenuTypeDuplicateException


class MenuTypeCommandService:
    @inject()
    def __init__(self, menutype_repo: MenuTypeRepo):
        self.menutype_repo = menutype_repo

    async def create_menutype(self, menutype: str, desc: str) -> MenuTypeSchema:
        if await self.menutype_repo.get(menutype):
            raise MenuTypeDuplicateException
        data_create = MenuType.create(menutype=menutype, desc=desc)
        data_saved = await self.menutype_repo.save(menutype=data_create)
        return data_saved

    async def update_menutype(self, menutype_id: int, menutype: Union[str, None], desc: Union[str, None]) -> MenuTypeSchema:
        data_get = await self.menutype_repo.get_by_id(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException
        if await self.menutype_repo.get(menutype):
            raise MenuTypeDuplicateException

        updates = {}
        if menutype:
            updates["menutype"] = menutype
        if desc:
            updates["desc"] = desc

        data_updated = await self.menutype_repo.update(data_get, updates)
        return data_updated

    async def delete_menutype(self, menutype_id: int, username: str) -> None:
        data_get = await self.menutype_repo.get_by_id(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException

        await self.menutype_repo.delete(data_get, username)
