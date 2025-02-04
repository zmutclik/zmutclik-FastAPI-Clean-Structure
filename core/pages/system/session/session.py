import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse, EnumJS

from core.exceptions import ForbiddenException
from core.app.logs.service import LogsQueryService
from core.app.security.client.service import ClientService
from core.app.security.session.service import SessionService

from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/session")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_system_session(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_system_session_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def page_system_session_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await SessionService().datatable_session(params=params)

@router.delete("/{PathCheck}/{id:int}", status_code=202, dependencies=page.depend_d())
async def kill_session(id: int, req: page_req):
    data_get = await SessionService().get_session(id)
    if data_get is None:
        raise ForbiddenException

    await SessionService().update_session(data_get.id, active=False)