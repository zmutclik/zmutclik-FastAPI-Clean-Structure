from typing import Union, Optional, Any
from pythondi import inject

from ..domain import User
from ..exceptions import UserNotFoundException, UserNotActiveException
from ..repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from ..schema import UserSchema


class UserQueryService:
    @inject()
    def __init__(
        self,
        user_repo: UserRepo,
        user_privilege_repo: UserPrivilegeRepo,
        user_scope_repo: UserScopeRepo,
    ):
        self.user_repo = user_repo
        self.user_privilege_repo = user_privilege_repo
        self.user_scope_repo = user_scope_repo

    async def get_user(self, user_id: str) -> Optional[UserSchema]:
        data_get = await self.user_repo.get(user_id)
        if not data_get:
            raise UserNotFoundException
        return data_get

    async def get_user_privileges(self, user_id: str):
        data_get = await self.user_privilege_repo.get_by_user(user_id)
        return data_get

    async def get_user_scopes(self, user_id: str):
        data_get = await self.user_scope_repo.get_by_user(user_id)
        return data_get

    async def get_user_by(
        self,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        nohp: Union[str, None] = None,
    ) -> Optional[UserSchema]:
        data_get = await self.user_repo.get_by(username, email, nohp)
        return data_get

    async def datatable(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_auth

        query = select(User, User.id.label("DT_RowId")).where(User.deleted_at == None)
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "username", "email", "nohp", "full_name", "disabled"],
            engine=session_auth,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()

    async def verify_password(self, user: User, plain_password: str) -> bool:
        return user.verify_password(plain_password)
