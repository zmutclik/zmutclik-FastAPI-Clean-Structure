import os
from enum import Enum
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

from core.app.auth.scope.service import ScopeCommandService, ScopeQueryService

from .request import ScopeRequest
from .response import ScopeReponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/scope")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


@router.get("", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_scope(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_scope_form_add(req: page_req):
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{scope_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_scope_form_edit(scope_id: int, req: page_req):
    page.addContext("data_scope", await ScopeQueryService().get_scope(scope_id))
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_js_scope(req: page_req, pathFile: PathJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def datatables_scope(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await ScopeQueryService().datatable_scope(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=ScopeReponse, dependencies=page.depend_w())
async def create_scope(dataIn: ScopeRequest, req: page_req):
    data_get = await ScopeQueryService().get_scope_by(scope=dataIn.scope)
    if data_get is not None:
        errors = [{"loc": ["body", "scope"], "msg": "duplicate scope is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await ScopeCommandService().create_scope(creted_user=req.user.username, scope=dataIn.scope, desc=dataIn.desc)
    return data_created


@router.post("/{PathCheck}/{scope_id:int}", status_code=201, response_model=ScopeReponse, dependencies=page.depend_w())
async def update_scope(scope_id: int, dataIn: ScopeRequest, req: page_req):
    data_get = await ScopeQueryService().get_scope(scope_id)

    if dataIn.scope != data_get.scope:
        data_filter = await ScopeQueryService().get_scope_by(scope=dataIn.scope)
        if data_filter is not None:
            errors = [{"loc": ["body", "scope"], "msg": "duplicate scope is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await ScopeCommandService().update_scope(scope_id=scope_id, scope=dataIn.scope, desc=dataIn.desc)
    return data_updated


@router.delete("/{PathCheck}/{scope_id:int}", status_code=202, dependencies=page.depend_d())
async def delete_scope(scope_id: int, req: page_req):
    await ScopeQueryService().get_scope(scope_id)
    await ScopeCommandService().delete_scope(scope_id, req.user.username)
