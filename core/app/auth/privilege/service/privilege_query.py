from typing import Union, Optional, Any
from pythondi import inject

from core.exceptions import NotFoundException
from ..domain import Privilege
from ..repository import PrivilegeRepo, PrivilegeMenusRepo
from ..schema import PrivilegeSchema, PrivilegeMenuSchema


class PrivilegeQueryService:
    @inject()
    def __init__(
        self,
        privilege_repo: PrivilegeRepo,
        privilege_menu_repo: PrivilegeMenusRepo,
    ):
        self.privilege_repo = privilege_repo
        self.privilege_menu_repo = privilege_menu_repo

    async def get_privilege(self, privilege_id: int) -> Optional[PrivilegeSchema]:
        data_get = await self.privilege_repo.get_privilege(privilege_id)
        if not data_get:
            raise NotFoundException("Privilege not found")
        return data_get

    async def get_privilege_by(self, privilege: str) -> Optional[PrivilegeSchema]:
        data_get = await self.privilege_repo.get_privilege(privilege)
        return data_get

    async def get_privileges(self) -> list[PrivilegeSchema]:
        return await self.privilege_repo.get_privileges()

    async def get_privilege_menus(self, privilege_id: int) -> list[PrivilegeMenuSchema]:
        return await self.privilege_menu_repo.get_privilege_menus(privilege_id=privilege_id)

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
        await datatable.generate()
        return datatable.output_result()
