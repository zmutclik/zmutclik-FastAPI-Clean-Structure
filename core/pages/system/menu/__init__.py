from fastapi import APIRouter

from .menu import router as router_menu
from .menutype import router as router_menutype

menu_router = APIRouter()
menu_router.include_router(router_menutype, tags=["SYS / MENUTYPE"])
menu_router.include_router(router_menu, tags=["SYS / MENU"])


__all__ = ["menu_router"]
