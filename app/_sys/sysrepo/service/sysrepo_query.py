from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session import async_engine
from app._sys.sysrepo.domain import SysRepo
from app._sys.sysrepo.repository import SysRepoRepo
from app._sys.sysrepo.schema import SysRepoSchema
from app._sys.sysrepo.exceptions import SysRepoNotFoundException


class SysRepoQueryService:
    @inject()
    def __init__(self, sysrepo_repo: SysRepoRepo):
        self.sysrepo_repo = sysrepo_repo

    async def get_sysrepo_by_id(self, sysrepo_id: str) -> Optional[SysRepoSchema]:
        data_get = self.sysrepo_repo.get_by_id(sysrepo_id)
        if not data_get:
            raise SysRepoNotFoundException
        return data_get

    async def get_sysrepo_active(self, allocation: str) -> Optional[SysRepoSchema]:
        data_get = self.sysrepo_repo.get_active(allocation=allocation)
        if not data_get:
            raise SysRepoNotFoundException
        return data_get

    async def get_sysrepo_by(self, allocation: str, name: str) -> Optional[SysRepoSchema]:
        data_get = self.sysrepo_repo.get_by(allocation=allocation, name=name)
        if not data_get:
            raise SysRepoNotFoundException
        return data_get

    async def datatable_sysrepo(self, params: dict[str, Any]):
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
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
