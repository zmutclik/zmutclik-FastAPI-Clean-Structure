from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine
from app._sys.crossorigin.domain import CrossOrigin
from app._sys.crossorigin.repository import CrossOriginRepo
from app._sys.crossorigin.schema import CrossOriginSchema
from app._sys.crossorigin.exceptions import CrossOriginNotFoundException


class CrossOriginQueryService:
    @inject()
    def __init__(self, crossorigin_repo: CrossOriginRepo):
        self.crossorigin_repo = crossorigin_repo

    async def get_crossorigin_by_id(self, crossorigin_id: str) -> Optional[CrossOriginSchema]:
        data_get = self.crossorigin_repo.get_crossorigin(crossorigin_id)
        if not data_get:
            raise CrossOriginNotFoundException
        return data_get

    async def get_crossorigin(self, link: str) -> Optional[CrossOriginSchema]:
        data_get = self.crossorigin_repo.get_crossorigin_by(link)
        if not data_get:
            raise CrossOriginNotFoundException
        return data_get

    async def datatable_crossorigin(self, params: dict[str, Any]):
        query = select(CrossOrigin, CrossOrigin.id.label("DT_RowId")).where(CrossOrigin.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "linkÏ"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
