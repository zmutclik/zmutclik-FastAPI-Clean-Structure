from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session import async_engine
from app._sys.menutype.domain import MenuType
from app._sys.menutype.repository import MenuTypeRepo
from app._sys.menutype.schema import MenuTypeSchema
from app._sys.menutype.exceptions import MenuTypeNotFoundException


class MenuTypeQueryService:
    @inject()
    def __init__(self, menutype_repo: MenuTypeRepo):
        self.menutype_repo = menutype_repo

    async def get_menutype_by_id(self, menutype_id: str) -> Optional[MenuTypeSchema]:
        data_get = self.menutype_repo.get_by_id(menutype_id)
        if not data_get:
            raise MenuTypeNotFoundException
        return data_get

    async def get_menutype(self, menutype: str) -> Optional[MenuTypeSchema]:
        data_get = self.menutype_repo.get(menutype)
        if not data_get:
            raise MenuTypeNotFoundException
        return data_get

    async def get_all_menutype(self) -> list[MenuTypeSchema]:
        data_get = self.menutype_repo.get_all()
        if not data_get:
            raise MenuTypeNotFoundException
        return data_get

    async def datatable_menutype(self, params: dict[str, Any]):
        query = select(MenuType, MenuType.id.label("DT_RowId")).where(MenuType.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "menutype", "desc"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
