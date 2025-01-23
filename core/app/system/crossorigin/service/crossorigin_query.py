from typing import Optional, Any
from pythondi import inject

from ..domain import CrossOrigin
from ..repository import CrossOriginRepo
from ..schema import CrossOriginSchema
from ..exceptions import CrossOriginNotFoundException


class CrossOriginQueryService:
    @inject()
    def __init__(self, crossorigin_repo: CrossOriginRepo):
        self.crossorigin_repo = crossorigin_repo

    async def get_crossorigin(self, crossorigin_id: int) -> Optional[CrossOriginSchema]:
        data_get = await self.crossorigin_repo.get_crossorigin(crossorigin_id)
        if not data_get:
            raise CrossOriginNotFoundException
        return data_get

    async def get_crossorigin_by(self, link: str) -> Optional[CrossOriginSchema]:
        return await self.crossorigin_repo.get_crossorigin_by(link)

    async def datatable_crossorigin(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_core

        query = select(CrossOrigin, CrossOrigin.id.label("DT_RowId")).where(CrossOrigin.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "link"],
            engine=session_core,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
