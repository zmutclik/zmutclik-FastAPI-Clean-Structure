from typing import Union
from pythondi import inject

from ..domain import Scope
from ..repository import ScopeRepo
from ..schema import ScopeSchema
from ..exceptions import ScopeNotFoundException, ScopeDuplicateException


class ScopeCommandService:
    @inject()
    def __init__(self, scope_repo: ScopeRepo):
        self.scope_repo = scope_repo

    async def create_scope(self, scope: str, desc: str) -> ScopeSchema:
        if await self.scope_repo.get_scope_by(scope):
            raise ScopeDuplicateException
        data_create = Scope.create(scope=scope, desc=desc)
        data_saved = await self.scope_repo.save_scope(scope=data_create)
        return data_saved

    async def update_scope(self, scope_id: int, scope: Union[str, None], desc: Union[str, None]) -> ScopeSchema:
        data_get = await self.scope_repo.get_scope(scope_id)
        if not data_get:
            raise ScopeNotFoundException
        if await self.scope_repo.get_scope_by(scope):
            raise ScopeDuplicateException

        updates = {}
        if scope:
            updates["scope"] = scope
        if desc:
            updates["desc"] = desc

        data_updated = await self.scope_repo.update_scope(data_get, updates)
        return data_updated

    
    async def delete_scope(self, scope_id: int,username:str) -> None:
        data_get = await self.scope_repo.get_scope(scope_id)
        if not data_get:
            raise ScopeNotFoundException
        
        await self.scope_repo.delete_scope(data_get, username)
