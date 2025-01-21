from typing import Union, Optional, Any
from pythondi import inject
from datetime import datetime

from core.app.logs.domain import Logs


class LogsQueryService:
    @inject()
    def __init__(self):
        pass

    async def datatable_logs(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from sqlalchemy.ext.asyncio import AsyncSession
        from core.db.session_logs import async_engine

        tahunbulan = datetime.strptime(params["search"]["time_start"], "%Y-%m-%d %H:%M:%S")

        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = select(Logs, Logs.id.label("DT_RowId"))
                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=["DT_RowId", "id", "client_id"],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
