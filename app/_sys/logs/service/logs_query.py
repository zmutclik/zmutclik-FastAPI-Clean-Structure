from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine
from app._sys.logs.domain import Logs
from app._sys.logs.repository import LogsRepo
from app._sys.logs.schema import LogsSchema


class LogsQueryService:
    @inject()
    def __init__(self, logs_repo: LogsRepo):
        self.logs_repo = logs_repo

    async def datatable_logs(self, params: dict[str, Any]):
        query = select(Logs, Logs.id.label("DT_RowId"))
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "client_id"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
