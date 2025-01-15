import os
from enum import Enum
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from pages.response import PageResponse

from core.app.auth.privilege.service import PrivilegeQueryService, PrivilegeCommandService
from core.app.menu.menu.service import MenuQueryService
from core.app.menu.menutype.service import MenuTypeQueryService

from .request import PrivilegeRequest
from .response import PrivilegeResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/sys/privilege")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix, depend_roles=["admin"])
page_req = Annotated[PageResponse, Depends(page.request)]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_privilege(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/menu/{menutype_id:int}/{privilege_id:int}", status_code=200)
async def data_menus(privilege_id: int, menutype_id: int, req: page_req):
    data_privilege_menu = await PrivilegeQueryService().get_privilege_menus(privilege_id=privilege_id)
    list_privilege_menu = []
    for item in data_privilege_menu:
        list_privilege_menu.append(item.menu_id)
    data_menus = await MenuQueryService().get_menus(menutype_id=menutype_id)
    res = []
    for item in data_menus:
        dt = {
            "id": str(item.id),
            "text": item.text,
            "icon": item.icon,
            "parent": "#" if item.parent_id == 0 else str(item.parent_id),
            "state": {"opened": True, "disabled": item.disabled, "selected": True if item.id in list_privilege_menu else False},
        }
        res.append(dt)
    return res


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_form_add_privilege(req: page_req):
    page.addContext("menutype", await MenuTypeQueryService().get_menutypes())
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{privilege_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_form_edit_privilege(privilege_id: int, req: page_req):
    page.addContext("menutype", await MenuTypeQueryService().get_menutypes())
    page.addContext("data_privilege", await PrivilegeQueryService().get_privilege(privilege_id))
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_js_privilege(req: page_req, pathFile: PathJS, privilege_id: int = 0):
    page.addContext("privilege_id", privilege_id)
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def datatables_privilege(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await PrivilegeQueryService().datatable_privilege(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=PrivilegeResponse, dependencies=page.depend_w())
async def create_privilege(dataIn: PrivilegeRequest, req: page_req):
    data_filter = await PrivilegeQueryService().get_privilege_by(privilege=dataIn.privilege)
    if data_filter is not None:
        errors = [{"loc": ["body", "privilege"], "msg": "duplicate privilege name is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await PrivilegeCommandService().create_privilege(
        created_user=req.user.username,
        privilege=dataIn.privilege,
        desc=dataIn.desc,
        menutype_id=dataIn.menutype_id,
        menus=dataIn.menus,
    )
    return data_created


@router.post("/{PathCheck}/{privilege_id:int}", status_code=201, response_model=PrivilegeResponse, dependencies=page.depend_w())
async def update_privilege(privilege_id: int, dataIn: PrivilegeRequest, req: page_req):
    data_get = await PrivilegeQueryService().get_privilege(privilege_id=privilege_id)

    if dataIn.privilege != data_get.privilege:
        data_filter = await PrivilegeQueryService().get_privilege_by(privilege=dataIn.privilege)
        if data_filter is not None:
            errors = [{"loc": ["body", "privilege"], "msg": "duplicate privilege name is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await PrivilegeCommandService().update_privilege(
        privilege_id=privilege_id,
        privilege=dataIn.privilege,
        desc=dataIn.desc,
        menutype_id=dataIn.menutype_id,
        menus=dataIn.menus,
    )
    return data_updated


@router.delete("/{PathCheck}/{privilege_id:int}", status_code=202, dependencies=page.depend_d())
async def delete_privilege(privilege_id: int, req: page_req):
    await PrivilegeQueryService().get_privilege(privilege_id)
    await PrivilegeCommandService().delete_privilege(privilege_id, req.user.username)
