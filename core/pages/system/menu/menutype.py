import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse, EnumJS

from core.app.menu.menutype.service import MenuTypeQueryService, MenuTypeCommandService

from .request import MenuTypeRequest
from .response import MenuTypeResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/menutype")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["admin"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_system_menutype(req: page_req):
    return page.response(req, "/html/menutype/index.html")


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_menutype_form_add(req: page_req):
    return page.response(req, "/html/menutype/form.html")


@router.get("/{PathCheck}/{menutype_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_menutype_form_edit(menutype_id: int, req: page_req):
    page.addContext("data_menutype", await MenuTypeQueryService().get_menutype(menutype_id))
    return page.response(req, "/html/menutype/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_system_menutype_js(req: page_req, pathFile: EnumJS):
    page.addContext("prefix_url_menu", "/page/sys/menu/" + req.user.client_id + "." + req.user.session_id)
    return page.response(req, "/html/menutype/" + pathFile)


# #######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def page_system_menutype_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await MenuTypeQueryService().datatable_menutype(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=MenuTypeResponse, dependencies=page.depend_w())
async def page_system_menutype_create(dataIn: MenuTypeRequest, req: page_req):
    data_filter = await MenuTypeQueryService().get_menutype_by(menutype=dataIn.menutype)
    if data_filter is not None:
        errors = [{"loc": ["body", "privilege"], "msg": "duplicate paket menu name is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await MenuTypeCommandService().create_menutype(
        created_user=req.user.username,
        menutype=dataIn.menutype,
        desc=dataIn.desc,
    )
    return data_created


@router.post("/{PathCheck}/{menutype_id:int}", status_code=201, response_model=MenuTypeResponse, dependencies=page.depend_w())
async def page_system_menutype_update(menutype_id: int, dataIn: MenuTypeRequest, req: page_req):
    data_get = await MenuTypeQueryService().get_menutype(menutype_id)

    if dataIn.menutype != data_get.menutype:
        data_filter = await MenuTypeQueryService().get_menutype_by(menutype=dataIn.menutype)
        if data_filter is not None:
            errors = [{"loc": ["body", "privilege"], "msg": "duplicate menutype name is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await MenuTypeCommandService().update_menutype(
        menutype_id=menutype_id,
        menutype=dataIn.menutype,
        desc=dataIn.desc,
    )
    return data_updated
