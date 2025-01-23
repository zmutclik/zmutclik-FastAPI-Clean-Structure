import os
from enum import Enum
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse, EnumJS

from core.app.system.coresystem.service import CoreSYSTEMService
from core.app.system.coresystem.schema import CoreSYSTEMSchema

router = APIRouter(prefix="/coresetting")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_coresetting(req: page_req):
    page.addContext("prefix_url_crossorigin", "/page/sys/crossorigin/" + req.user.client_id + "." + req.user.session_id)
    page.addContext("prefix_url_changelog", "/page/sys/changelog/" + req.user.client_id + "." + req.user.session_id)
    page.addContext("data_coresystem", await CoreSYSTEMService().get_coresystem())
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_coresetting_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}", status_code=201, response_model=CoreSYSTEMSchema, dependencies=page.depend_w())
async def page_system_coresetting_update(dataIn: CoreSYSTEMSchema, req: page_req):
    data_updated = await CoreSYSTEMService().update_coresystem(dataIn)
    return data_updated
