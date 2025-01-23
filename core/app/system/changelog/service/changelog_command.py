from typing import Union
from pythondi import inject
from datetime import date

from ..domain import ChangeLog
from ..repository import ChangeLogRepo
from ..schema import ChangeLogSchema
from ..exceptions import ChangeLogDuplicateException, ChangeLogNotFoundException


class ChangeLogCommandService:
    @inject()
    def __init__(self, changelog_repo: ChangeLogRepo):
        self.changelog_repo = changelog_repo

    async def create_changelog(self, created_user: str, dateupdate: date, version_name: str, description: str) -> ChangeLogSchema:
        if await self.changelog_repo.get_changelog_by(version_name=version_name):
            raise ChangeLogDuplicateException
        date_create = ChangeLog.create(
            created_user=created_user,
            dateupdate=dateupdate,
            version_name=version_name,
            description=description,
        )
        data_saved = await self.changelog_repo.save_changelog(changelog=date_create)
        return data_saved

    async def update_changelog(
        self,
        changelog_id: int,
        dateupdate: Union[date, None],
        version_name: Union[str, None],
        desc: Union[str, None],
    ) -> ChangeLogSchema:
        data_get = await self.changelog_repo.get_changelog(changelog_id)
        if not data_get:
            raise ChangeLogNotFoundException
        if await self.changelog_repo.get_changelog_by(version_name):
            raise ChangeLogDuplicateException

        updates = {}
        if dateupdate:
            updates["dateupdate"] = dateupdate
        if version_name:
            updates["version_name"] = version_name
        if desc:
            updates["desc"] = desc

        data_updated = await self.changelog_repo.update_changelog(data_get, updates)
        return data_updated

    async def delete_changelog(self, changelog_id: int, username: str) -> None:
        data_get = await self.changelog_repo.get_changelog(changelog_id)
        if not data_get:
            raise ChangeLogNotFoundException

        await self.changelog_repo.delete_changelog(data_get, username)
