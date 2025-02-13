from pythondi import inject
from datetime import timedelta, datetime, timezone
import json

from core import config_auth
from core.fastapi.helper import token_jwt

from ....security.session.domain import Session
from ....security.session.service import SessionService

from ...scope.repository import ScopeRepo
from ...privilege.repository import PrivilegeRepo, PrivilegeMenusRepo

from ....menu.menu.service import MenuQueryService
from ....menu.menutype.service import MenuTypeQueryService

from ..domain import User
from ..repository import UserRepo, UserPrivilegeRepo, UserScopeRepo
from ..schema import UserSchema


class UserAuthService:
    @inject()
    def __init__(
        self,
        user_repo: UserRepo,
        user_privilege_repo: UserPrivilegeRepo,
        user_scope_repo: UserScopeRepo,
        privilege_repo: PrivilegeRepo,
        privilege_menu_repo: PrivilegeMenusRepo,
        scope_repo: ScopeRepo,
    ):
        self.user_repo = user_repo
        self.user_privilege_repo = user_privilege_repo
        self.user_scope_repo = user_scope_repo
        self.privilege_repo = privilege_repo
        self.privilege_menu_repo = privilege_menu_repo
        self.scope_repo = scope_repo

    async def token_create(self, jwt_secret: str, user: User, session_id: str):
        roles = []
        scopes = []
        roles_by_id = await self.user_privilege_repo.get_userprivileges(user.id)
        scope_by_id = await self.user_scope_repo.get_userscopes(user.id)

        for item in roles_by_id:
            dataget = await self.privilege_repo.get_privilege(item.privilege_id)
            roles.append(dataget.privilege)
        for item in scope_by_id:
            dataget = await self.scope_repo.get_scope(item.scope_id)
            scopes.append(dataget.scope)

        access_token = token_jwt(
            jwt_secret,
            data={
                "sub": user.username,
                "roles": roles,
                "permissions": scopes,
                "jti": session_id,
            },
            expires_delta=timedelta(minutes=config_auth.COOKIES_EXPIRED),
        )
        return access_token

    async def refresh_create(self, user: User, client_id: str, session_id: str) -> str:
        access_token = token_jwt(
            config_auth.JWT_SECRET_KEY,
            data={
                "sub": user.username,
                "client": client_id,
                "session": session_id,
            },
            expires_delta=timedelta(minutes=config_auth.REFRESH_EXPIRED),
        )
        return access_token

    async def generate_cache_user(self, user: User) -> None:
        user_schema = UserSchema.model_validate(user.__dict__)
        with open(".db/cache/user/{}.json".format(user.username), "w") as outfile:
            outfile.write(user_schema.model_dump_json())

    async def generate_cache_menu(self, user: User) -> None:
        list_privilege = await self.user_privilege_repo.get_userprivileges(user.id)
        list_filter_menu_id = []
        is_privilege_system = False
        for item in list_privilege:
            PrivilegeMenus = await self.privilege_menu_repo.get_privilege_menus(item.privilege_id)
            if item.privilege_id == 3:
                is_privilege_system = True
            if PrivilegeMenus:
                for item in PrivilegeMenus:
                    list_filter_menu_id.append(item.menu_id)

        if is_privilege_system:
            list_filter_menu_id = None

        for item in await MenuTypeQueryService().get_menutypes():
            menus = await MenuQueryService().generate_menus(item.id, 0, list_filter_menu_id)
            menus_json = json.dumps([menu.model_dump() for menu in menus], indent=4)
            with open(".db/cache/menu/{}_{}.json".format(user.username, item.menutype), "w") as outfile:
                outfile.write(menus_json)
