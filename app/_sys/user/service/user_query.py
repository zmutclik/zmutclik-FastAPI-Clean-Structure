from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session_ import async_engine, dbapps_engine
from app._sys.user.domain import User
from app._sys.user.repository import UserRepo
from app._sys.user.schema import UserSchema
from app._sys.user.exceptions import UserNotFoundException, UserNotActiveException


class UserQueryService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_user(self, user_id: str) -> Optional[UserSchema]:
        data_get = await self.user_repo.get(user_id)
        if not data_get:
            raise UserNotFoundException
        return data_get

    async def get_user_by(
        self,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        nohp: Union[str, None] = None,
    ) -> Optional[UserSchema]:
        data_get = await self.user_repo.get_by(username, email, nohp)
        # if not data_get:
        #     raise UserNotFoundException
        # if data_get.disabled:
        #     raise UserNotActiveException

        return data_get

    async def datatable(self, params: dict[str, Any]):
        query = select(User, User.id.label("DT_RowId")).where(User.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "username", "email", "nohp", "full_name", "disabled"],
            engine=dbapps_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
