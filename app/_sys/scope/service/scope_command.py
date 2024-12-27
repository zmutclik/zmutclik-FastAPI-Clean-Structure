from typing import Union
from pythondi import inject

from app._sys.scope.domain import Scope
from app._sys.scope.repository import ScopeRepo
from app._sys.scope.schema import ScopeSchema
from app._sys.scope.exceptions import ScopeNotFoundException, ScopeDuplicateException


class ScopeCommandService:
    @inject()
    def __init__(self, scope_repo: ScopeRepo):
        self.scope_repo = scope_repo

    async def create(self, scope: str, desc: str) -> ScopeSchema:
        if await self.scope_repo.get(scope):
            raise ScopeDuplicateException
        data_create = Scope.create(scope=scope, desc=desc)
        data_saved = await self.scope_repo.save(privilege=data_create)
        return data_saved

    async def update(self, scope_id: int, scope: Union[str, None], desc: Union[str, None]) -> ScopeSchema:
        data_get = await self.scope_repo.get_by_id(scope_id)
        if not data_get:
            raise ScopeNotFoundException
        if await self.scope_repo.get(scope):
            raise ScopeDuplicateException

        updates = {}
        if scope:
            updates["scope"] = scope
        if desc:
            updates["desc"] = desc

        data_updated = await self.scope_repo.update(data_get, updates)
        return data_updated

    
    async def delete(self, scope_id: int,username:str) -> None:
        data_get = await self.scope_repo.get_by_id(scope_id)
        if not data_get:
            raise ScopeNotFoundException
        
        await self.scope_repo.delete(data_get, username)
