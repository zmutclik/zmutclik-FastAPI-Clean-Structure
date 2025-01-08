from pythondi import inject
from datetime import timedelta
import random
import string

from app._sys.user.domain import User, UserPrivilege, UserScope
from app._sys.user.repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from app._sys.user.schema import UserSchema
from app._sys.user.exceptions import DuplicateEmailOrNicknameOrNoHPException, UserNotFoundException
from core import config
from core.fastapi.service import token_create


class UserAuthService:
    @inject()
    def __init__(self, user_repo: UserRepo, user_privilege_repo: UserPrivilegeRepo, user_scope_repo: UserScopeRepo):
        self.user_repo = user_repo
        self.user_privilege_repo = user_privilege_repo
        self.user_scope_repo = user_scope_repo

    async def token_create(self, user: User) -> str:
        roles = await self.user_privilege_repo.get_list_by_user(user.id)
        scopes = await self.user_scope_repo.get_list_by_user(user.id)

        access_token = token_create(
            data={
                "sub": user.username,
                "roles": roles,
                "permissions": scopes,
                "jti": "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))),
            },
            expires_delta=timedelta(minutes=config.COOKIES_EXPIRED),
        )

        return access_token
