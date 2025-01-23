from typing import Union
from pythondi import inject

from ..domain import CrossOrigin
from ..repository import CrossOriginRepo
from ..schema import CrossOriginSchema
from ..exceptions import CrossOriginNotFoundException, CrossOriginDuplicateException


class CrossOriginCommandService:
    @inject()
    def __init__(self, crossorigin_repo: CrossOriginRepo):
        self.crossorigin_repo = crossorigin_repo

    async def create_crossorigin(self, created_user: str, link: str) -> CrossOriginSchema:
        if await self.crossorigin_repo.get_crossorigin_by(link):
            raise CrossOriginDuplicateException
        data_create = CrossOrigin.create(created_user=created_user, link=link)
        data_saved = await self.crossorigin_repo.save_crossorigin(crossorigin=data_create)
        return data_saved

    async def update_crossorigin(self, crossorigin_id: int, link: Union[str, None]) -> CrossOriginSchema:
        data_get = await self.crossorigin_repo.get_crossorigin(crossorigin_id)
        if not data_get:
            raise CrossOriginNotFoundException
        if await self.crossorigin_repo.get_crossorigin_by(link):
            raise CrossOriginDuplicateException

        updates = {}
        if link:
            updates["link"] = link

        data_updated = await self.crossorigin_repo.update_crossorigin(data_get, updates)
        return data_updated

    async def delete_crossorigin(self, crossorigin_id: int, username: str) -> None:
        data_get = await self.crossorigin_repo.get_crossorigin(crossorigin_id)
        if not data_get:
            raise CrossOriginNotFoundException

        await self.crossorigin_repo.delete_crossorigin(data_get, username)
