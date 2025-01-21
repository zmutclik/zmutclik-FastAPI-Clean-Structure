from typing import Union, Optional, Any
from pythondi import inject

from core.db.session_ import async_engine
from ..domain import SysRepo
from ..repository import SysRepoRepo
from ..schema import SysRepoSchema
from ..exceptions import SysRepoNotFoundException


class SysRepoQueryService:
    @inject()
    def __init__(self, sysrepo_repo: SysRepoRepo):
        self.sysrepo_repo = sysrepo_repo

    async def get_sysrepo(self, sysrepo_id: int) -> Optional[SysRepoSchema]:
        data_get = await self.sysrepo_repo.get_sysrepo(sysrepo_id)
        if not data_get:
            raise SysRepoNotFoundException
        return data_get

    async def get_sysrepo_active(self, allocation: str) -> Optional[SysRepoSchema]:
        data_get = await self.sysrepo_repo.get_sysrepo_active(allocation=allocation)
        if not data_get:
            raise SysRepoNotFoundException
        return data_get

    async def get_sysrepo_by(self, allocation: str, name: str) -> Optional[SysRepoSchema]:
        data_get = await self.sysrepo_repo.get_sysrepo_by(allocation=allocation, name=name)
        return data_get

    async def datatable_sysrepo(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_core

        query = select(SysRepo, SysRepo.id.label("DT_RowId")).where(SysRepo.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=[
                "DT_RowId",
                "id",
                "name",
                "allocation",
                "datalink",
                "user",
                "is_active",
            ],
            engine=session_core,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
