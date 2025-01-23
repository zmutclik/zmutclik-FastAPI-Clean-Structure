import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse, EnumJS

from core.app.logs.service import LogsQueryService

from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/logs")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_logs(req: page_req):
    page.addContext("data_ipaddress", await LogsQueryService().get_ipaddress())
    page.addContext("data_routername", await LogsQueryService().get_routers_name())
    page.addContext("data_username", await LogsQueryService().get_username())
    page.addContext("data_clientid", await LogsQueryService().get_clientid())
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_logs_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_w())
async def page_system_logs_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await LogsQueryService().datatable_logs(params=params)
