from typing import Union, Optional, Any
from pythondi import inject

from ..domain import User
from ..exceptions import UserNotFoundException
from ..repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from ..schema import UserSchema
from fastapi.exceptions import RequestValidationError


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
        data_get = await self.user_repo.get_user(user_id)
        if not data_get:
            raise UserNotFoundException
        return data_get

    async def get_user_privileges(self, user_id: int):
        data_get = await self.user_privilege_repo.get_userprivileges(user_id)
        return data_get

    async def get_user_privilege(self, user_id: int, privilege_id: int):
        return await self.user_privilege_repo.get_userprivilege_by(user_id, privilege_id)

    async def get_user_scopes(self, user_id: int):
        data_get = await self.user_scope_repo.get_userscopes(user_id)
        return data_get

    async def get_user_by(
        self, username: Union[str, None] = None, email: Union[str, None] = None, nohp: Union[str, None] = None
    ) -> Optional[UserSchema]:
        return await self.user_repo.get_user_by(username, email, nohp)

    async def validate_user(self, username: str = None, email: str = None, nohp: str = None) -> None:
        errors = []

        if username is not None:
            data_filter_user = await UserQueryService().get_user_by(username=username)
            if data_filter_user is not None:
                errors.append({"loc": ["body", "username"], "msg": f"duplicate username {username} is use", "type": "value_error.duplicate"})
        if email is not None:
            data_filter_emil = await UserQueryService().get_user_by(email=email)
            if data_filter_emil is not None:
                errors.append({"loc": ["body", "email"], "msg": f"duplicate email {email} is use", "type": "value_error.duplicate"})
        if nohp is not None:
            data_filter_nohp = await UserQueryService().get_user_by(nohp=nohp)
            if data_filter_nohp is not None:
                errors.append({"loc": ["body", "nohp"], "msg": f"duplicate nohp {nohp} is use", "type": "value_error.duplicate"})

        if len(errors) > 0:
            raise RequestValidationError(errors)

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
