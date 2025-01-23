from typing import Optional, Any
from pythondi import inject

from ..domain import ChangeLog
from ..repository import ChangeLogRepo
from ..schema import ChangeLogSchema
from ..exceptions import ChangeLogNotFoundException


class ChangeLogQueryService:
    @inject()
    def __init__(self, changelog_repo: ChangeLogRepo):
        self.changelog_repo = changelog_repo

    async def get_changelog(self, privilege_id: int) -> Optional[ChangeLogSchema]:
        data_get = await self.changelog_repo.get_changelog(privilege_id)
        if not data_get:
            raise ChangeLogNotFoundException
        return data_get

    async def get_changelog_by(self, version_name: str) -> Optional[ChangeLogSchema]:
        return await self.changelog_repo.get_changelog_by(version_name)

    async def datatable_changelog(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_core

        query = select(ChangeLog, ChangeLog.id.label("DT_RowId")).where(ChangeLog.deleted_at == None).order_by(ChangeLog.dateupdate.desc(), ChangeLog.id.desc())
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "dateupdate", "version_name", "description", "created_user"],
            engine=session_core,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
