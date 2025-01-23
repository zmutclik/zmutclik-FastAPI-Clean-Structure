import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from core.pages.response import PageResponse, EnumJS

from core.app.system.crossorigin.service import CrossOriginQueryService, CrossOriginCommandService

from .request import CrossOriginRequest

router = APIRouter(prefix="/crossorigin")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_crossorigin_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/crossorigin/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_w())
async def page_system_crossorigin_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await CrossOriginQueryService().datatable_crossorigin(params=params)


@router.post("/{PathCheck}", status_code=201, dependencies=page.depend_w())
async def page_system_crossorigin_create(dataIn: CrossOriginRequest, req: page_req):
    data_get = await CrossOriginQueryService().get_crossorigin_by(link=str(dataIn.link))
    if data_get is not None:
        errors = [{"loc": ["body", "link"], "msg": "duplicate link is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)
    await CrossOriginCommandService().create_crossorigin(link=str(dataIn.link), created_user=req.user.username)


@router.delete("/{PathCheck}/{crossorigin_id:int}", status_code=202, dependencies=page.depend_d())
async def page_system_crossorigin_delete(crossorigin_id: int, req: page_req):
    await CrossOriginQueryService().get_crossorigin(crossorigin_id)
    await CrossOriginCommandService().delete_crossorigin(crossorigin_id, req.user.username)
