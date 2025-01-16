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

    async def get_menu_by_id(self, menu_id: str) -> Optional[MenuSchema]:
        data_get = await self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException
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

    async def generate_menus(self, menutype_id: int, parent_id: int = 0, filter_menu: list[int] = []):
        menus_result = []
        data_get = await self.menu_repo.get_menus_by(menutype_id, parent_id)
        for item in data_get:
            menu_validate = MenuViewSchema.model_validate(item.__dict__)
            menu_json = menu_validate.model_dump()
            if menu_json["tooltip"] is None:
                menu_json["tooltip"] = ""
            menu_json["children"] = []

            data_child = await self.menu_repo.get_menus_by(menutype_id, item.id)
            if len(data_child) > 0:
                menu_json["children"] = await self.generate_menus(menutype_id, item.id, filter_menu)

            if item.id in filter_menu and not menu_validate.disabled:
                menus_result.append(menu_json)

        return menus_result
