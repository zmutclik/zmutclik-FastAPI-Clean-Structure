from typing import Union, Optional, Any
from pythondi import inject
from datetime import datetime

from core.app.logs.domain import Logs
from core.app.logs.repository import LogsRepo


class LogsQueryService:

    async def get_ipaddress(self, tahunbulan: datetime = None):
        return await LogsRepo().get_ipaddress(tahunbulan=tahunbulan)

    async def get_routers_name(self, tahunbulan: datetime = None):
        return await LogsRepo().get_routers_name(tahunbulan=tahunbulan)

    async def get_username(self, tahunbulan: datetime = None):
        return await LogsRepo().get_username(tahunbulan=tahunbulan)

    async def get_clientid(self, tahunbulan: datetime = None):
        return await LogsRepo().get_clientid(tahunbulan=tahunbulan)

    async def get_logerror(self, logerror_id: int, tahunbulan: datetime = None):
        return await LogsRepo().get_logerror(logerror_id=logerror_id, tahunbulan=tahunbulan)

    async def datatable_logs(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from sqlalchemy.ext.asyncio import AsyncSession
        from core.db.session_logs import async_engine

        tahunbulan = datetime.strptime(params["search"]["bulantahun"], "%Y-%m-%d %H:%M:%S")

        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = select(Logs, Logs.id.label("DT_RowId")).filter(
                    Logs.startTime >= params["search"]["time_start"],
                    Logs.startTime <= params["search"]["time_end"],
                )

                if params["search"]["ipaddress"] != "":
                    query = query.filter(Logs.ipaddress.like("%" + params["search"]["ipaddress"] + "%"))

                if params["search"]["method"] != "":
                    query = query.filter(Logs.method == params["search"]["method"])

                if params["search"]["status"] != "":
                    query = query.filter(Logs.status_code.like(params["search"]["status"] + "%"))

                if params["search"]["path"] != "":
                    query = query.filter(Logs.path.like("%" + params["search"]["path"] + "%"))

                if params["search"]["referer"] != "":
                    query = query.filter(Logs.referer.like("%" + params["search"]["referer"] + "%"))

                if params["search"]["routername"] != "":
                    query = query.filter(Logs.router == params["search"]["routername"])

                if params["search"]["clientid"] != "":
                    query = query.filter(Logs.client_id == params["search"]["clientid"])

                if params["search"]["username"] != "":
                    query = query.filter(Logs.user == params["search"]["username"])

                if params["search"]["channel"] != "":
                    if params["search"]["channel"] == "None":
                        query = query.filter(Logs.channel == None)
                    else:
                        query = query.filter(Logs.channel == params["search"]["channel"])

                query = query.order_by(Logs.startTime.desc())

                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=[
                        "DT_RowId",
                        "id",
                        "startTime",
                        "client_id",
                        "platform",
                        "browser",
                        "path",
                        "referer",
                        "method",
                        "ipaddress",
                        "user",
                        "status_code",
                        "process_time",
                        "process_time",
                    ],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
