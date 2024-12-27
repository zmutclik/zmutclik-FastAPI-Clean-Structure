from pythondi import Provider, configure

from app._sys.user.repository import UserRepo, UserSQLRepo, UserPrivilegeRepo, UserPrivilegeSQLRepo
from app._sys.privilege.repository import PrivilegeRepo, PrivilegeSQLRepo


def init_di():
    provider = Provider()
    provider.bind(UserRepo, UserSQLRepo)
    provider.bind(UserPrivilegeRepo, UserPrivilegeSQLRepo)
    provider.bind(PrivilegeRepo, PrivilegeSQLRepo)
    configure(provider=provider)
