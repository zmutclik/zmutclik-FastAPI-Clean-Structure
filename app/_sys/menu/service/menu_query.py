from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine
from app._sys.menu.domain import Menu
from app._sys.menu.repository import MenuRepo
from app._sys.menu.schema import MenuSchema
from app._sys.menu.exceptions import MenuNotFoundException


class MenuQueryService:
    @inject()
    def __init__(self, menu_repo: MenuRepo):
        self.menu_repo = menu_repo

    async def get_menu_by_id(self, menu_id: str) -> Optional[MenuSchema]:
        data_get = self.menu_repo.get_menu(menu_id)
        if not data_get:
            raise MenuNotFoundException
        return data_get

    async def get_menus(self, menutype_id: int) -> list[MenuSchema]:
        data_get = self.menu_repo.get_menu_by(menutype_id)
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
