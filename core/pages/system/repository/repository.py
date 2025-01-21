import os
from enum import Enum
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

from core.app.system.sysrepo.service import SysRepoCommandService, SysRepoQueryService

from .request import SysRepoRequest
from .response import SysRepoResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/repository")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


@router.get("", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_repository(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_repository_form_add(req: page_req):
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{repository_id:int}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_repository_form_edit(repository_id: int, req: page_req):
    page.addContext("data_repository", await SysRepoQueryService().get_sysrepo(repository_id))
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_js_repository(req: page_req, pathFile: PathJS):
    return page.response(req, "/html/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def datatables_repository(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await SysRepoQueryService().datatable_sysrepo(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=SysRepoResponse, dependencies=page.depend_w())
async def create_repository(dataIn: SysRepoRequest, req: page_req):
    data_get = await SysRepoQueryService().get_sysrepo_by(allocation=dataIn.allocation, name=dataIn.name)
    if data_get is not None:
        errors = [{"loc": ["body", "name"], "msg": "duplicate name of allocation is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await SysRepoCommandService().create_sysrepo(
        name=dataIn.name,
        allocation=dataIn.allocation,
        datalink=dataIn.datalink,
        user=dataIn.user,
        password=dataIn.password,
        created_user=req.user.username,
    )
    return data_created


@router.post("/{PathCheck}/{repository_id:int}", status_code=201, response_model=SysRepoResponse, dependencies=page.depend_w())
async def update_repository(repository_id: int, dataIn: SysRepoRequest, req: page_req):
    data_get = await SysRepoQueryService().get_sysrepo(repository_id)
    if dataIn.name != data_get.name and dataIn.allocation == data_get.allocation:
        data_filter = await SysRepoQueryService().get_sysrepo_by(allocation=dataIn.allocation, name=dataIn.name)
        if data_filter is not None:
            errors = [{"loc": ["body", "name"], "msg": "duplicate name of allocation is use", "type": "value_error.duplicate"}]
            raise RequestValidationError(errors)

    data_updated = await SysRepoCommandService().update_sysrepo(
        sysrepo_id=repository_id,
        name=dataIn.name,
        datalink=dataIn.datalink,
        user=dataIn.user,
        password=dataIn.password,
    )
    return data_updated


@router.delete("/{PathCheck}/{repository_id:int}", status_code=202, dependencies=page.depend_d())
async def delete_repository(repository_id: int, req: page_req):
    await SysRepoQueryService().get_sysrepo(repository_id)
    await SysRepoCommandService().delete_sysrepo(repository_id, req.user.username)
