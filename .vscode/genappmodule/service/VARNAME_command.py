from typing import Union
from pythondi import inject

from ..domain import CLASSNAME
from ..repository import CLASSNAMERepo
from ..schema import CLASSNAMESchema
from ..exceptions import CLASSNAMENotFoundException, CLASSNAMEDuplicateException


class CLASSNAMECommandService:
    @inject()
    def __init__(self, VARNAME_repo: CLASSNAMERepo):
        self.VARNAME_repo = VARNAME_repo

    async def create_VARNAME(self, VARNAME: str) -> CLASSNAMESchema:
        if await self.VARNAME_repo.get_VARNAME_by(VARNAME):
            raise CLASSNAMEDuplicateException
        data_create = CLASSNAME.create(VARNAME=VARNAME)
        data_saved = await self.VARNAME_repo.save_VARNAME(VARNAME=data_create)
        return data_saved

    async def update_VARNAME(self, VARNAME_id: int, VARNAME: Union[str, None]) -> CLASSNAMESchema:
        data_get = await self.VARNAME_repo.get_VARNAME(VARNAME_id)
        if not data_get:
            raise CLASSNAMENotFoundException
        if await self.VARNAME_repo.get_VARNAME(VARNAME):
            raise CLASSNAMEDuplicateException

        updates = {}
        if VARNAME:
            updates["VARNAME"] = VARNAME

        data_updated = await self.VARNAME_repo.update_VARNAME(data_get, **updates)
        return data_updated

    async def delete_VARNAME(self, VARNAME_id: int, username: str) -> None:
        data_get = await self.VARNAME_repo.get_VARNAME(VARNAME_id)
        if not data_get:
            raise CLASSNAMENotFoundException

        await self.VARNAME_repo.delete_VARNAME(data_get, username)
