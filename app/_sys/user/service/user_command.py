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

        data_create = User.create(
            username=username,
            email=email,
            nohp=nohp,
            full_name=full_name,
            password1=password1,
            password2=password2,
        )
        data_saved = await self.user_repo.save(user=data_create)

        for item in privileges:
            user_privilege = UserPrivilege.create(data_saved.id, item)
            await self.user_privilege_repo.save(user_privilege=user_privilege)

        await self.user_privilege_repo.commit()

        return data_saved

    async def update_user_password(self, user_id: int, password1: str, password2: str) -> UserSchema:
        data_get = await self.user_repo.get(user_id)
        if not data_get:
            raise UserNotFoundException
        data_updated = data_get.change_password(password1, password2)
        return data_updated

    async def update_user(
        self,
        user_id: int,
        email: Union[str, None],
        nohp: Union[str, None],
        full_name: Union[str, None],
        privileges: list[int],
    ) -> UserSchema:
        data_get = await self.user_repo.get(user_id)
        if not data_get:
            raise UserNotFoundException

        updates = {}
        if full_name:
            updates["full_name"] = full_name
        if email:
            updates["email"] = email
        if nohp:
            updates["nohp"] = nohp

        data_updated = await self.user_repo.update(data_get, updates)

        await self.user_privilege_repo.delete_in_user(user_id=user_id)
        for item in privileges:
            user_privilege = UserPrivilege.create(user_id, item)
            await self.user_privilege_repo.save(user_privilege=user_privilege)
        await self.user_privilege_repo.commit()

        return data_updated

    
    async def delete_user(self, user_id: int,username:str) -> None:
        data_get = await self.user_repo.get(user_id)
        if not data_get:
            raise UserNotFoundException
        
        await self.user_repo.delete(data_get, username)
