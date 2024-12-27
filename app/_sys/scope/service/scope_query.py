from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session import async_engine
from app._sys.scope.domain import Scope
from app._sys.scope.repository import ScopeRepo
from app._sys.scope.schema import ScopeSchema
from app._sys.scope.exceptions import ScopeNotFoundException


class PrivilegeQueryService:
    @inject()
    def __init__(self, scope_repo: ScopeRepo):
        self.scope_repo = scope_repo

    async def privilege_get_by_id(self, scope_id: str) -> Optional[ScopeSchema]:
        data_get = self.scope_repo.get_by_id(scope_id)
        if not data_get:
            raise ScopeNotFoundException
        return ScopeSchema.model_validate(data_get)

    async def privilege_get(self, scope: str) -> Optional[ScopeSchema]:
        data_get = self.privilege_repo.get(scope)
        if not data_get:
            raise ScopeNotFoundException
        return ScopeSchema.model_validate(data_get)

    async def datatable(self, params: dict[str, Any]):
        query = select(Scope, Scope.id.label("DT_RowId")).where(Scope.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "scope", "desc"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
