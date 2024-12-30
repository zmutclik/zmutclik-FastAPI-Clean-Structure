from typing import Union
from pythondi import inject
from datetime import date

from app._sys.changelog.domain import ChangeLog
from app._sys.changelog.repository import ChangeLogRepo
from app._sys.changelog.schema import ChangeLogSchema
from app._sys.changelog.exceptions import ChangeLogDuplicateException, ChangeLogNotFoundException


class ChangeLogCommandService:
    @inject()
    def __init__(self, changelog_repo: ChangeLogRepo):
        self.changelog_repo = changelog_repo

    async def create_changelog(self, dateupdate: date, version_name: str, desc: str) -> ChangeLogSchema:
        if await self.changelog_repo.get(version_name):
            raise ChangeLogDuplicateException
        date_create = ChangeLog.create(
            dateupdate=dateupdate,
            version_name=version_name,
            desc=desc,
        )
        data_saved = await self.changelog_repo.save(changelog=date_create)
        return data_saved

    async def update_changelog(
        self,
        changelog_id: int,
        dateupdate: Union[date, None],
        version_name: Union[str, None],
        desc: Union[str, None],
    ) -> ChangeLogSchema:
        data_get = await self.changelog_repo.get_by_id(changelog_id)
        if not data_get:
            raise ChangeLogNotFoundException
        if await self.changelog_repo.get(version_name):
            raise ChangeLogDuplicateException

        updates = {}
        if dateupdate:
            updates["dateupdate"] = dateupdate
        if version_name:
            updates["version_name"] = version_name
        if desc:
            updates["desc"] = desc

        data_updated = await self.changelog_repo.update(data_get, updates)
        return data_updated

    async def delete_changelog(self, changelog_id: int, username: str) -> None:
        data_get = await self.changelog_repo.get_by_id(changelog_id)
        if not data_get:
            raise ChangeLogNotFoundException

        await self.changelog_repo.delete(data_get, username)
