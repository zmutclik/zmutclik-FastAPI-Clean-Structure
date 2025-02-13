from sqlalchemy.orm import Session
from core.config import DBSECURITY_FILE
from ._func import check_exits, check_sizes


def securitydb_create_all():
    check_exits(DBSECURITY_FILE)
    if check_sizes(DBSECURITY_FILE):
        from core.config import dbsecurity_engine
        from ..base import BaseSecuriry as Base
        from core.app.security.client.domain import Client, ClientUser, ClientUserOtp, ClientUserResetCode
        from core.app.security.session.domain import Session
        from core.app.security.clientsso.domain import ClientSSO, ClientSSO_code

        Base.metadata.create_all(bind=dbsecurity_engine)
