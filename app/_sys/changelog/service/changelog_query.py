from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine
from app._sys.changelog.domain import ChangeLog
from app._sys.changelog.repository import ChangeLogRepo
from app._sys.changelog.schema import ChangeLogSchema
from app._sys.changelog.exceptions import ChangeLogNotFoundException


class ChangeLogQueryService:
    @inject()
    def __init__(self, changelog_repo: ChangeLogRepo):
        self.changelog_repo = changelog_repo

    async def get_changelog_by_id(self, privilege_id: str) -> Optional[ChangeLogSchema]:
        data_get = self.changelog_repo.get_by_id(privilege_id)
        if not data_get:
            raise ChangeLogNotFoundException
        return data_get

    async def get_changelog(self, privilege: str) -> Optional[ChangeLogSchema]:
        data_get = self.changelog_repo.get(privilege)
        if not data_get:
            raise ChangeLogNotFoundException
        return data_get

    async def datatable_changelog(self, params: dict[str, Any]):
        query = select(ChangeLog, ChangeLog.id.label("DT_RowId")).where(ChangeLog.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "dateupdate", "version_name", "desc"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
