from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session import async_engine
from app.VARNAME.domain import CLASSNAME
from app.VARNAME.repository import CLASSNAMERepo
from app.VARNAME.schema import CLASSNAMESchema
from app.VARNAME.exceptions import CLASSNAMENotFoundException


class CLASSNAMEQueryService:
    @inject()
    def __init__(self, VARNAME_repo: CLASSNAMERepo):
        self.VARNAME_repo = VARNAME_repo

    async def get_VARNAME_by_id(self, VARNAME_id: str) -> Optional[CLASSNAMESchema]:
        data_get = self.VARNAME_repo.get_by_id(VARNAME_id)
        if not data_get:
            raise CLASSNAMENotFoundException
        return data_get

    async def get_VARNAME(self, VARNAME: str) -> Optional[CLASSNAMESchema]:
        data_get = self.VARNAME_repo.get(VARNAME)
        if not data_get:
            raise CLASSNAMENotFoundException
        return data_get

    async def datatable_VARNAME(self, params: dict[str, Any]):
        query = select(CLASSNAME, CLASSNAME.id.label("DT_RowId")).where(CLASSNAME.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "VARNAME"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()