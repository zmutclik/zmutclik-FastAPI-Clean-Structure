from typing import Union
from pythondi import inject

from app._sys.menu.domain import Menu
from app._sys.menu.repository import MenuRepo
from app._sys.menu.schema import MenuSchema
from app._sys.menu.exceptions import MenuNotFoundException, MenuDuplicateException


class MenuCommandService:
    @inject()
    def __init__(self, menu_repo: MenuRepo):
        self.menu_repo = menu_repo

    async def create_menu(
        self,
        text: str,
        segment: str,
        tooltip: str,
        href: str,
        icon: str,
        icon_color: str,
        menutype_id: int,
    ) -> MenuSchema:
        data_create = Menu.create(
            text=text,
            segment=segment,
            tooltip=tooltip,
            href=href,
            icon=icon,
            icon_color=icon_color,
            menutype_id=menutype_id,
        )
        data_saved = await self.menu_repo.save_menu(menu=data_create)
        return data_saved

    async def update_menu(
        self,
        menu_id: int,
        text: Union[str, None],
        segment: Union[str, None],
        tooltip: Union[str, None],
        href: Union[str, None],
        icon: Union[str, None],
        icon_color: Union[str, None],
        sort: Union[int, None],
        parent_id: Union[int, None],
        disabled: Union[bool, None],
    ) -> MenuSchema:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException

        updates = {}
        if text:
            updates["text"] = text
        if segment:
            updates["segment"] = segment
        if tooltip:
            updates["tooltip"] = tooltip
        if href:
            updates["href"] = href
        if icon:
            updates["icon"] = icon
        if icon_color:
            updates["icon"] = icon_color
        if sort:
            updates["sort"] = sort
        if parent_id:
            updates["parent_id"] = parent_id
        if disabled:
            updates["disabled"] = disabled

        data_updated = await self.menu_repo.update_menu(data_get, updates)
        return data_updated

    async def delete_menu(self, menu_id: int, username: str) -> None:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException

        await self.menu_repo.delete_menu(data_get, username)
