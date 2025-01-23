from pythondi import Provider, configure

from core.app.system.changelog.repository import ChangeLogRepo, ChangeLogRepoSQLRepo
from core.app.system.crossorigin.repository import CrossOriginRepo, CrossOriginSQLRepo
from core.app.menu.menu.repository import MenuRepo, MenuSQLRepo
from core.app.menu.menutype.repository import MenuTypeRepo, MenuTypeSQLRepo
from core.app.auth.privilege.repository import PrivilegeRepo, PrivilegeSQLRepo, PrivilegeMenusRepo, PrivilegeMenusSQLRepo
from core.app.auth.scope.repository import ScopeRepo, ScopeSQLRepo
from core.app.system.sysrepo.repository import SysRepoRepo, SysRepoSQLRepo
from core.app.auth.user.repository import UserRepo, UserSQLRepo, UserPrivilegeRepo, UserPrivilegeSQLRepo, UserScopeRepo, UserScopeSQLRepo
from core.app.system.coresystem.repository import CoreSYSTEMRepo, CoreSYSTEMSQLRepo


def init_di():
    provider = Provider()
    provider.bind(ChangeLogRepo, ChangeLogRepoSQLRepo)
    provider.bind(CrossOriginRepo, CrossOriginSQLRepo)
    provider.bind(MenuRepo, MenuSQLRepo)
    provider.bind(MenuRepo, MenuSQLRepo)
    provider.bind(MenuTypeRepo, MenuTypeSQLRepo)
    provider.bind(PrivilegeRepo, PrivilegeSQLRepo)
    provider.bind(PrivilegeMenusRepo, PrivilegeMenusSQLRepo)
    provider.bind(ScopeRepo, ScopeSQLRepo)
    provider.bind(SysRepoRepo, SysRepoSQLRepo)
    provider.bind(UserRepo, UserSQLRepo)
    provider.bind(UserPrivilegeRepo, UserPrivilegeSQLRepo)
    provider.bind(UserScopeRepo, UserScopeSQLRepo)
    provider.bind(CoreSYSTEMRepo, CoreSYSTEMSQLRepo)
    configure(provider=provider)
