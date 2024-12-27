from typing import Union
from pythondi import inject

from app._sys.user.domain import User, UserPrivilege
from app._sys.user.repository import UserRepo, UserPrivilegeRepo
from app._sys.user.schema import UserSchema
from app._sys.user.exceptions import DuplicateEmailOrNicknameOrNoHPException, UserNotFoundException


class UserCommandService:
    @inject()
    def __init__(self, user_repo: UserRepo, user_privilege_repo: UserPrivilegeRepo):
        self.user_repo = user_repo
        self.user_privilege_repo = user_privilege_repo

    async def create_user(
        self,
        username: str,
        email: str,
        nohp: str,
        full_name: str,
        password1: str,
        password2: str,
        privileges: list[int],
    ) -> UserSchema:
        if await self.user_repo.get_by(username, email, nohp):
            raise DuplicateEmailOrNicknameOrNoHPException

        user = User.create(
            username=username,
            email=email,
            nohp=nohp,
            full_name=full_name,
            password1=password1,
            password2=password2,
        )
        user = await self.user_repo.save(user=user)

        for item in privileges:
            user_privilege = UserPrivilege.create(user.id, item)
            await self.user_privilege_repo.save(user_privilege=user_privilege)

        await self.user_privilege_repo.commit()

        return UserSchema.model_validate(user)

    async def update_password(self, user_id: int, password1: str, password2: str) -> UserSchema:
        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundException
        user = user.change_password(password1, password2)
        return UserSchema.model_validate(user)

    async def update(
        self,
        user_id: int,
        email: Union[str, None],
        nohp: Union[str, None],
        full_name: Union[str, None],
        privileges: list[int],
    ) -> UserSchema:
        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundException

        updates = {}
        if full_name:
            updates["full_name"] = full_name
        if email:
            updates["email"] = email
        if nohp:
            updates["nohp"] = nohp

        user = await self.user_repo.update(user, updates)

        await self.user_privilege_repo.delete_in_user(user_id=user_id)
        for item in privileges:
            user_privilege = UserPrivilege.create(user_id, item)
            await self.user_privilege_repo.save(user_privilege=user_privilege)
        await self.user_privilege_repo.commit()

        return UserSchema.model_validate(user)
