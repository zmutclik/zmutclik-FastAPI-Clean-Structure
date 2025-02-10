from sqlalchemy.orm import Session
from core.config import DBAUTH_FILE
from ._func import check_exits, check_sizes


def authdb_create_all():
    check_exits(DBAUTH_FILE)
    if check_sizes(DBAUTH_FILE):
        from core.config import dbauth_engine
        from ..base import BaseAuth as Base
        from core.app.auth.user.domain import User, UserPrivilege, UserScope
        from core.app.auth.privilege.domain import Privilege
        from core.app.auth.scope.domain import Scope

        Base.metadata.create_all(bind=dbauth_engine)
        with dbauth_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    User(
                        **{
                            "username": "admin",
                            "email": "admin@test.id",
                            "nohp": "62812345678",
                            "full_name": "Admin SeMuT",
                            "hashed_password": "$2b$12$ofIPPqnjPf54SzEvctr3DOzNqyjZQqDaA3GraVDvBobo/UfjtGqQm",
                            "created_user": "SeMuT-CiLiK",
                            "disabled": False,
                        }
                    )
                )
                db.add(Scope(**{"scope": "read", "desc": "", "created_user": "SeMuT-CiLiK"}))
                db.add(Scope(**{"scope": "write", "desc": "", "created_user": "SeMuT-CiLiK"}))
                db.add(Scope(**{"scope": "delete", "desc": "", "created_user": "SeMuT-CiLiK"}))
                db.add(Privilege(**{"privilege": "user", "desc": "Privilage Standart Users", "created_user": "SeMuT-CiLiK"}))
                db.add(Privilege(**{"privilege": "admin", "desc": "Privilage Khusus Administrator Applikasi", "created_user": "SeMuT-CiLiK"}))
                db.add(Privilege(**{"privilege": "system", "desc": "Privilage Khusus Administrator Core System", "created_user": "SeMuT-CiLiK"}))
                db.add(UserPrivilege(**{"user_id": 1, "privilege_id": 1}))
                db.add(UserPrivilege(**{"user_id": 1, "privilege_id": 2}))
                db.add(UserPrivilege(**{"user_id": 1, "privilege_id": 3}))
                db.add(UserScope(**{"user_id": 1, "scope_id": 1}))
                db.add(UserScope(**{"user_id": 1, "scope_id": 2}))
                db.add(UserScope(**{"user_id": 1, "scope_id": 3}))
                db.commit()
