from pythondi import Provider, configure

from app._sys.changelog.repository import ChangeLogRepo, ChangeLogRepoSQLRepo
from app._sys.crossorigin.repository import CrossOriginRepo, CrossOriginSQLRepo
from app._sys.logs.repository import LogsRepo, LogsSQLRepo
from app._sys.menu.repository import MenuRepo, MenuSQLRepo
from app._sys.menutype.repository import MenuTypeRepo, MenuTypeSQLRepo
from app._sys.privilege.repository import PrivilegeRepo, PrivilegeSQLRepo
from app._sys.scope.repository import ScopeRepo, ScopeSQLRepo
from app._sys.sysrepo.repository import SysRepoRepo, SysRepoSQLRepo
from app._sys.user.repository import UserRepo, UserSQLRepo, UserPrivilegeRepo, UserPrivilegeSQLRepo


def init_di():
    provider = Provider()
    provider.bind(ChangeLogRepo, ChangeLogRepoSQLRepo)
    provider.bind(CrossOriginRepo, CrossOriginSQLRepo)
    provider.bind(LogsRepo, LogsSQLRepo)
    provider.bind(MenuRepo, MenuSQLRepo)
    provider.bind(MenuRepo, MenuSQLRepo)
    provider.bind(MenuTypeRepo, MenuTypeSQLRepo)
    provider.bind(PrivilegeRepo, PrivilegeSQLRepo)
    provider.bind(ScopeRepo, ScopeSQLRepo)
    provider.bind(SysRepoRepo, SysRepoSQLRepo)
    provider.bind(UserRepo, UserSQLRepo)
    provider.bind(UserPrivilegeRepo, UserPrivilegeSQLRepo)
    configure(provider=provider)
