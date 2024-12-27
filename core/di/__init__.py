from pythondi import Provider, configure

from app._sys.user.repository import UserRepo, UserSQLRepo, UserPrivilegeRepo, UserPrivilegeSQLRepo
from app._sys.privilege.repository import PrivilegeRepo, PrivilegeSQLRepo
from app._sys.scope.repository import ScopeRepo, ScopeSQLRepo


def init_di():
    provider = Provider()
    provider.bind(UserRepo, UserSQLRepo)
    provider.bind(UserPrivilegeRepo, UserPrivilegeSQLRepo)
    provider.bind(PrivilegeRepo, PrivilegeSQLRepo)
    provider.bind(ScopeRepo, ScopeSQLRepo)
    configure(provider=provider)
