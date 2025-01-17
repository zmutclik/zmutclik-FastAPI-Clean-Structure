from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine
from ..domain import Menu
from ..repository import MenuRepo
from ..schema import MenuSchema, MenuViewSchema
from ..exceptions import MenuNotFoundException


class MenuQueryService:
    @inject()
    def __init__(self, menu_repo: MenuRepo):
        self.menu_repo = menu_repo

    async def get_menu(self, menu_id: int) -> Optional[MenuSchema]:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException
        return data_get

    async def get_menu_by(self, menutype_id: int, text: str) -> Optional[MenuSchema]:
        data_get = await self.menu_repo.get_menu_by(menutype_id, text)
        return data_get

    async def get_menus(self, menutype_id: int) -> list[MenuSchema]:
        data_get = await self.menu_repo.get_menus(menutype_id=menutype_id)
        if not data_get:
            raise MenuNotFoundException
        return data_get

    async def datatable_menu(self, menutype_id: int, params: dict[str, Any]):
        query = (
            select(Menu, Menu.id.label("DT_RowId"))
            .where(
                Menu.menutype_id == menutype_id,
                Menu.deleted_at == None,
            )
            .order_by(Menu.sort)
        )
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=[
                "DT_RowId",
                "id",
                "text",
                "segment",
                "href",
                "icon",
                "disabled",
            ],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()

    async def generate_menus(self, menutype_id: int, parent_id: int = 0, filter_menu: list[int] = [])->MenuViewSchema:
        menus_result = []
        data_get = await self.menu_repo.get_menus_by(menutype_id, parent_id)
        for item in data_get:
            menu_validate = MenuViewSchema.model_validate(item.__dict__)
            if menu_validate.tooltip is None:
                menu_validate.tooltip = ""

            data_child = await self.menu_repo.get_menus_by(menutype_id, item.id)
            if len(data_child) > 0:
                menu_validate.children = await self.generate_menus(menutype_id, item.id, filter_menu)

            if filter_menu is None:
                menus_result.append(menu_validate)
            elif item.id in filter_menu and not menu_validate.disabled:
                menus_result.append(menu_validate)

        return menus_result
