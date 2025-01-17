import os
from enum import Enum
from typing import Annotated, Any,List
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

from core.app.menu.menu.service import MenuQueryService, MenuCommandService
from core.app.menu.menu.exceptions import MenuNotFoundException

from .request import MenuRequest
from .response import MenuResponse, MenusResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/menu")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["admin"])
page_req = Annotated[PageResponse, Depends(page.request)]


class PathJS(str, Enum):
    detailJs = "detail.js"


@router.get("/{PathCheck}/{menutype_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_menu(menutype_id: int, req: page_req):
    page.addContext("menutype_id", menutype_id)
    return page.response(req, "/html/menu/detail.html")


@router.get("/{PathCheck}/{menutype_id:int}/menus", response_model=List[MenusResponse], status_code=200)
async def get_menus_data(menutype_id: int, req: page_req):
    return await MenuQueryService().generate_menus(menutype_id=menutype_id, filter_menu=None)


@router.get("/{PathCheck}/{menutype_id:int}/{menu_id:int}", response_model=MenuResponse, status_code=200)
async def get_menu_data(menutype_id: int, menu_id: int, req: page_req):
    data_get = await MenuQueryService().get_menu(menu_id)
    if data_get.menutype_id != menutype_id:
        raise MenuNotFoundException
    return data_get


@router.get("/{PathCheck}/{menutype_id:int}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_js_privilege(menutype_id: int, req: page_req, pathFile: PathJS):
    page.addContext("prefix_url_menutype", "/page/sys/menutype")
    page.addContext("menutype_id", menutype_id)
    return page.response(req, "/html/menu/" + pathFile)


#######################################################################################################################
async def menu_sorting_save(parent_id: int, dataIn: List[MenusResponse]):
    i = 0
    for item in dataIn:
        i = i + 1
        await MenuCommandService().update_menu(menu_id=item.id, parent_id=parent_id, sort=i)
        if len(item.children) > 0:
            await menu_sorting_save(int(item.id), item.children)


@router.post("/{PathCheck}/{menutype_id:int}/menus", status_code=201, dependencies=page.depend_w())
async def menu_sorting(dataIn: List[MenusResponse], req: page_req):
    await menu_sorting_save( 0, dataIn)
    
    
@router.post("/{PathCheck}/{menutype_id:int}", status_code=201, response_model=MenuResponse, dependencies=page.depend_w())
async def create_menutype(menutype_id: int, dataIn: MenuRequest, req: page_req):
    data_filter = await MenuQueryService().get_menu_by(menutype_id=menutype_id, text=dataIn.text)
    if data_filter is not None:
        errors = [{"loc": ["body", "privilege"], "msg": "duplicate text label menu is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await MenuCommandService().create_menu(
        created_user=req.user.username,
        text=dataIn.text,
        segment=dataIn.segment,
        tooltip=dataIn.tooltip,
        href=dataIn.href,
        icon=dataIn.icon,
        # icon_color=dataIn.icon_color,
        menutype_id=menutype_id,
    )
    return data_created


@router.post("/{PathCheck}/{menutype_id:int}/{menu_id:int}", status_code=201, response_model=MenuResponse, dependencies=page.depend_w())
async def update_privilege(menutype_id: int, menu_id: int, dataIn: MenuRequest, req: page_req):
    data_get = await MenuQueryService().get_menu(menu_id)

    if dataIn.text != data_get.text:
        data_filter = await MenuQueryService().get_menu_by(menutype_id=menutype_id, text=dataIn.text)
        if data_filter is not None:
            errors = [{"loc": ["body", "privilege"], "msg": "duplicate text label menu is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await MenuCommandService().update_menu(
        menu_id=menu_id,
        text=dataIn.text,
        segment=dataIn.segment,
        tooltip=dataIn.tooltip,
        href=dataIn.href,
        icon=dataIn.icon,
        disabled=dataIn.disabled,
    )
    return data_updated

@router.delete("/{PathCheck}/{menutype_id:int}/{menu_id:int}", status_code=202)
async def menu_delete(menutype_id: int, menu_id: int,  req: page_req):
    await MenuCommandService().delete_menu(menu_id=menu_id, username=req.user.username)