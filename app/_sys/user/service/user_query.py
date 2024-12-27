from typing import Union, Optional, Any
from pythondi import inject

from sqlalchemy import or_, select
from datatables import DataTable

from core.db.session import async_engine
from app._sys.user.domain import User
from app._sys.user.repository import UserRepo
from app._sys.user.schema import UserSchema
from app._sys.user.exceptions import UserNotFoundException


class UserQueryService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def user_get(self, user_id: str) -> Optional[UserSchema]:
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundException
        return UserSchema.model_validate(user)

    async def user_get_by(self, username: Union[str, None], email: Union[str, None], nohp: Union[str, None]) -> Optional[UserSchema]:
        user = self.user_repo.get_by(username, email, nohp)
        if not user:
            raise UserNotFoundException

        return UserSchema.model_validate(user)

    async def datatable(self, params: dict[str, Any]):
        query = select(User, User.id.label("DT_RowId")).where(User.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "username", "email", "nohp", "full_name", "disabled"],
            engine=async_engine,
            # callbacks=callbacks,
        )
        return datatable.output_result()
