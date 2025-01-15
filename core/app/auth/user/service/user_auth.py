from pythondi import inject
from datetime import timedelta
import random
import string

from ..domain import User, UserPrivilege, UserScope
from ..repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from ...privilege.repository import PrivilegeRepo
from ...scope.repository import ScopeRepo
from ....menu.menu.service import MenuQueryService
from ..schema import UserSchema
from ..exceptions import DuplicateEmailOrNicknameOrNoHPException, UserNotFoundException
from core import config
from core.fastapi.service import token_create


class UserAuthService:
    @inject()
    def __init__(
        self,
        user_repo: UserRepo,
        user_privilege_repo: UserPrivilegeRepo,
        user_scope_repo: UserScopeRepo,
        privilege_repo: PrivilegeRepo,
        scope_repo: ScopeRepo,
    ):
        self.user_repo = user_repo
        self.user_privilege_repo = user_privilege_repo
        self.user_scope_repo = user_scope_repo
        self.privilege_repo = privilege_repo
        self.scope_repo = scope_repo

    async def token_create(self, user: User) -> str:
        roles = []
        scopes = []
        roles_by_id = await self.user_privilege_repo.get_by_user(user.id)
        scope_by_id = await self.user_scope_repo.get_by_user(user.id)

        for item in roles_by_id:
            dataget = await self.privilege_repo.get_privilege(item.privilege_id)
            roles.append(dataget.privilege)
        for item in scope_by_id:
            dataget = await self.scope_repo.get_scope(item.scope_id)
            scopes.append(dataget.scope)

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

    async def generate_cache_menu(self, user: User) -> None:
        list_privilege = await self.user_privilege_repo.get_by_user(user.id)
        for item in list_privilege:
            print(item.privilege_id)
            MenuQueryService().get_menus(item.pr)
        # print(list_privilege)
        pass
