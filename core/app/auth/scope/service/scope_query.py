from typing import Union, Optional, Any
from pythondi import inject

from core.exceptions import NotFoundException
from ..domain import Scope
from ..repository import ScopeRepo
from ..schema import ScopeSchema


class ScopeQueryService:
    @inject()
    def __init__(self, scope_repo: ScopeRepo):
        self.scope_repo = scope_repo

    async def get_scope(self, scope_id: int) -> Optional[ScopeSchema]:
        data_get = await self.scope_repo.get_scope(scope_id)
        if not data_get:
            raise NotFoundException("scope not found")
        return data_get

    async def get_scope_by(self, scope: str) -> Optional[ScopeSchema]:
        data_get = await self.scope_repo.get_scope_by(scope)
        return data_get

    async def get_scopes(self) -> list[ScopeSchema]:
        return await self.scope_repo.get_scopes()

    async def datatable_scope(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_auth

        query = select(Scope, Scope.id.label("DT_RowId")).where(Scope.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "scope", "desc"],
            engine=session_auth,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
