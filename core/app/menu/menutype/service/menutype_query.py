from typing import Union, Optional, Any
from pythondi import inject

from core.db.session_ import async_engine
from ..domain import MenuType
from ..repository import MenuTypeRepo
from ..schema import MenuTypeSchema
from ..exceptions import MenuTypeNotFoundException


class MenuTypeQueryService:
    @inject()
    def __init__(self, menutype_repo: MenuTypeRepo):
        self.menutype_repo = menutype_repo

    async def get_menutype(self, menutype_id: int) -> Optional[MenuTypeSchema]:
        data_get = await self.menutype_repo.get_menutype(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException
        return data_get

    async def get_menutype_by(self, menutype: str) -> Optional[MenuTypeSchema]:
        data_get = await self.menutype_repo.get_menutype_by(menutype)
        return data_get

    async def get_menutypes(self) -> list[MenuTypeSchema]:
        data_get = await self.menutype_repo.get_menutypes()
        if not data_get:
            raise MenuTypeNotFoundException
        return data_get

    async def datatable_menutype(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_menu

        query = select(MenuType, MenuType.id.label("DT_RowId")).where(MenuType.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "menutype", "desc"],
            engine=session_menu,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
