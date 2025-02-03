from typing import Union, Optional, Any
from pythondi import inject

from ..domain import CLASSNAME
from ..repository import CLASSNAMERepo
from ..schema import CLASSNAMESchema
from ..exceptions import CLASSNAMENotFoundException


class CLASSNAMEQueryService:
    @inject()
    def __init__(self, VARNAME_repo: CLASSNAMERepo):
        self.VARNAME_repo = VARNAME_repo

    async def get_VARNAME(self, VARNAME_id: str) -> Optional[CLASSNAMESchema]:
        data_get = self.VARNAME_repo.get_VARNAME(VARNAME_id)
        if not data_get:
            raise CLASSNAMENotFoundException
        return data_get

    async def get_VARNAME_by(self, VARNAME: str) -> Optional[CLASSNAMESchema]:
        return self.VARNAME_repo.get_VARNAME_by(VARNAME)

    async def datatable_VARNAME(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_

        query = select(CLASSNAME, CLASSNAME.id.label("DT_RowId")).where(CLASSNAME.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "VARNAME"],
            engine=session_,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
