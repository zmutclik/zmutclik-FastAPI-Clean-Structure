from typing import Union
from pythondi import inject

from ..domain import Menu
from ..repository import MenuRepo
from ..schema import MenuSchema
from ..exceptions import MenuNotFoundException


class MenuCommandService:
    @inject()
    def __init__(self, menu_repo: MenuRepo):
        self.menu_repo = menu_repo

    async def create_menu(
        self,
        created_user: str,
        text: str,
        segment: str,
        tooltip: str,
        href: str,
        icon: str,
        menutype_id: int,
        icon_color: Union[str, None] = None,
    ) -> MenuSchema:
        data_create = Menu.create(
            created_user=created_user,
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
        text: Union[str, None]=None,
        segment: Union[str, None]=None,
        tooltip: Union[str, None]=None,
        href: Union[str, None]=None,
        icon: Union[str, None]=None,
        disabled: Union[bool, None]=None,
        sort: Union[int, None]=None,
        parent_id: Union[int, None]=None,
        icon_color: Union[str, None]=None,
    ) -> MenuSchema:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException

        updates = {}
        if text is not None:
            updates["text"] = text
        if segment is not None:
            updates["segment"] = segment
        if tooltip is not None:
            updates["tooltip"] = tooltip
        if href is not None:
            updates["href"] = href
        if icon is not None:
            updates["icon"] = icon
        if icon_color is not None:
            updates["icon"] = icon_color
        if sort is not None:
            updates["sort"] = sort
        if parent_id is not None:
            updates["parent_id"] = parent_id
        if disabled is not None:
            updates["disabled"] = disabled

        data_updated = await self.menu_repo.update_menu(data_get, **updates)
        return data_updated

    async def delete_menu(self, menu_id: int, username: str) -> None:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException

        await self.menu_repo.delete_menu(data_get, username)
