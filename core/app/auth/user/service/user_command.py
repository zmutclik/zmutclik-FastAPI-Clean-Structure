from typing import Union
from pythondi import inject

from ..domain import User, UserPrivilege, UserScope
from ..exceptions import UserNotFoundException
from ..repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from ..schema import UserSchema


class UserCommandService:
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

    async def create_user(
        self,
        created_user: str,
        username: str,
        email: str,
        nohp: str,
        full_name: str,
        password1: str = None,
        password2: str = None,
        privileges: list[int] = [1],
        scopes: list[int] = [1],
    ) -> UserSchema:

        data_create = User.create(
            created_user=created_user,
            username=username,
            email=email,
            nohp=nohp,
            full_name=full_name,
            password1=password1,
            password2=password2,
        )
        data_saved = await self.user_repo.save_user(user=data_create)

        for item in privileges:
            user_privilege = UserPrivilege.create(data_saved.id, item)
            await self.user_privilege_repo.save_userprivilege(user_privilege=user_privilege)

        await self.user_privilege_repo.commit_userprivilege()

        for item in scopes:
            user_scope = UserScope.create(data_saved.id, item)
            await self.user_scope_repo.save_userscope(user_scope=user_scope)

        await self.user_scope_repo.commit_userscope()

        return data_saved

    async def update_user_password(self, user_id: int, password1: str, password2: str) -> UserSchema:
        data_get = await self.user_repo.get_user(user_id)
        if not data_get:
            raise UserNotFoundException
        data_updated = data_get.change_password(password1, password2)
        return data_updated

    async def update_user(
        self,
        user_id: int,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        nohp: Union[str, None] = None,
        full_name: Union[str, None] = None,
        disabled: Union[bool, None] = None,
        privileges: list[int] = [],
        scopes: list[int] = [],
    ) -> UserSchema:
        data_get = await self.user_repo.get_user(user_id)
        if not data_get:
            raise UserNotFoundException

        updates = {}
        if full_name is not None:
            updates["username"] = username
        if full_name is not None:
            updates["full_name"] = full_name
        if email is not None:
            updates["email"] = email
        if nohp is not None:
            updates["nohp"] = nohp
        if disabled is not None:
            updates["disabled"] = disabled

        data_updated = await self.user_repo.update_user(data_get, **updates)

        if privileges != []:
            await self.user_privilege_repo.delete_userprivileges(user_id=user_id)
            for item in privileges:
                user_privilege = UserPrivilege.create(user_id, item)
                await self.user_privilege_repo.save_userprivilege(user_privilege=user_privilege)
            await self.user_privilege_repo.commit_userprivilege()

        if scopes != []:
            await self.user_scope_repo.delete_userscopes(user_id=user_id)
            for item in scopes:
                user_scope = UserScope.create(user_id, item)
                await self.user_scope_repo.save_userscope(user_scope=user_scope)
            await self.user_scope_repo.commit_userscope()

        return data_updated

    async def delete_user(self, user_id: int, username: str) -> None:
        data_get = await self.user_repo.get_user(user_id)
        if not data_get:
            raise UserNotFoundException

        await self.user_repo.delete_user(data_get, username)
