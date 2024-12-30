from typing import Union
from pythondi import inject
from datetime import date

from app._sys.sysrepo.domain import SysRepo
from app._sys.sysrepo.repository import SysRepoRepo
from app._sys.sysrepo.schema import SysRepoSchema
from app._sys.sysrepo.exceptions import SysRepoDuplicateException, SysRepoNotFoundException


class SysRepoCommandService:
    @inject()
    def __init__(self, sysrepo_repo: SysRepoRepo):
        self.sysrepo_repo = sysrepo_repo

    async def create_sysrepo(self, name: str, allocation: str, datalink: str, user: str, password: str) -> SysRepoSchema:
        if await self.sysrepo_repo.get_by(allocation=allocation, name=name):
            raise SysRepoDuplicateException
        date_create = SysRepo.create(
            name=name,
            allocation=allocation,
            datalink=datalink,
            user=user,
            password=password,
        )
        data_saved = await self.sysrepo_repo.save(sysrepo=date_create)
        return data_saved

    async def update_sysrepo(
        self,
        sysrepo_id: int,
        name: Union[str, None],
        datalink: Union[str, None],
        user: Union[str, None],
        password: Union[str, None],
    ) -> SysRepoSchema:
        data_get = await self.sysrepo_repo.get_by_id(sysrepo_id)
        if not data_get:
            raise SysRepoNotFoundException
        if await self.sysrepo_repo.get_by(allocation=data_get.allocation, name=name):
            raise SysRepoDuplicateException

        updates = {}
        if name:
            updates["name"] = name
        if datalink:
            updates["datalink"] = datalink
        if user:
            updates["user"] = user
        if password:
            updates["password"] = password

        data_updated = await self.sysrepo_repo.update(data_get, updates)
        return data_updated

    async def delete_sysrepo(self, sysrepo_id: int, username: str) -> None:
        data_get = await self.sysrepo_repo.get_by_id(sysrepo_id)
        if not data_get:
            raise SysRepoNotFoundException

        await self.sysrepo_repo.delete(data_get, username)
