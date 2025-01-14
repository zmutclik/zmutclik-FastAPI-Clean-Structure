from typing import Union, Optional, Any
from pythondi import inject

from ..domain import Privilege
from ..repository import PrivilegeRepo
from ..schema import PrivilegeSchema
from ..exceptions import PrivilegeNotFoundException


class PrivilegeQueryService:
    @inject()
    def __init__(self, privilege_repo: PrivilegeRepo):
        self.privilege_repo = privilege_repo

    async def get_privilege_by_id(self, privilege_id: str) -> Optional[PrivilegeSchema]:
        data_get = await self.privilege_repo.get_privilege_by_id(privilege_id)
        if not data_get:
            raise PrivilegeNotFoundException
        return data_get

    async def get_privilege(self, privilege: str) -> Optional[PrivilegeSchema]:
        data_get = await self.privilege_repo.get_privilege(privilege)
        if not data_get:
            raise PrivilegeNotFoundException
        return data_get

    async def get_privileges(self) -> list[PrivilegeSchema]:
        return await self.privilege_repo.get_privileges()

    async def datatable_privilege(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_auth

        query = select(Privilege, Privilege.id.label("DT_RowId")).where(Privilege.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "privilege", "desc"],
            engine=session_auth,
            # callbacks=callbacks,
        )
        return datatable.output_result()
