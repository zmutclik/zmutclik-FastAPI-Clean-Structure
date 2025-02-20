from sqlalchemy.orm import Session
from core.config import DBMENU_FILE
from ._func import check_exits, check_sizes


def menudb_create_all():
    check_exits(DBMENU_FILE)
    if check_sizes(DBMENU_FILE):
        from core.config import dbmenu_engine
        from ..base import BaseMenu as Base
        from core.app.menu.menu.domain import Menu
        from core.app.menu.menutype.domain import MenuType

        Base.metadata.create_all(bind=dbmenu_engine)
        with dbmenu_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    MenuType(
                        **{
                            "menutype": "sidebar",
                            "desc": "Side Bar Menu",
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Dashboard",
                            "href": "/page/dashboard",
                            "segment": "dashboard",
                            "icon": "fas fa-tachometer-alt",
                            "icon_color": "",
                            "sort": 1,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Settings",
                            "segment": "settings",
                            "href": "#",
                            "icon": "fas fa-cogs",
                            "icon_color": "",
                            "sort": 2,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Akun",
                            "segment": "akun",
                            "href": "/page/settings/akun",
                            "icon_color": "",
                            "icon": "fas fa-house-user",
                            "sort": 1,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Hak Akses",
                            "segment": "privilege",
                            "href": "/page/settings/privilege",
                            "icon": "fas fa-object-group",
                            "icon_color": "",
                            "sort": 2,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "System Core",
                            "segment": "system",
                            "href": "#",
                            "icon": "fas fa-cogs",
                            "icon_color": "",
                            "sort": 3,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Setting Sistem",
                            "segment": "coresetting",
                            "href": "/page/sys/coresetting",
                            "icon": "fas fa-headset",
                            "icon_color": "",
                            "sort": 1,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Gudang Link",
                            "segment": "repository",
                            "href": "/page/sys/repository",
                            "icon": "fas fa-link",
                            "icon_color": "",
                            "sort": 2,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Scope",
                            "segment": "scope",
                            "href": "/page/sys/scope",
                            "icon": "fas fa-map-marker-alt",
                            "icon_color": "",
                            "sort": 3,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Menu",
                            "segment": "menu",
                            "href": "/page/sys/menutype",
                            "icon_color": "",
                            "icon": "fas fa-list-alt",
                            "sort": 4,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Session",
                            "segment": "session",
                            "href": "/page/sys/session",
                            "icon": "fas fa-door-open",
                            "icon_color": "",
                            "sort": 5,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Client SSO",
                            "segment": "clientsso",
                            "href": "/page/sys/client_sso",
                            "icon": "fas fa-user-lock",
                            "icon_color": "",
                            "sort": 6,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Message",
                            "segment": "message",
                            "href": "/page/sys/message",
                            "icon": "fas fa-envelope-open-text",
                            "icon_color": "",
                            "sort": 7,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Logs",
                            "segment": "logs",
                            "href": "/page/sys/logs",
                            "icon": "fas fa-map-marked-alt",
                            "icon_color": "",
                            "sort": 8,
                            "menutype_id": 1,
                            "parent_id": 5,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Page Documentation",
                            "segment": "documentation_page",
                            "href": "/page/documentation/page",
                            "icon": "fab fa-html5",
                            "icon_color": "",
                            "sort": 4,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "API Documentation",
                            "segment": "documentation_api",
                            "href": "/page/documentation/api",
                            "icon": "fas fa-file-code",
                            "icon_color": "",
                            "sort": 5,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.commit()
