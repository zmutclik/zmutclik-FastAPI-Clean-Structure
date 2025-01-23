import os
from datetime import datetime
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from core.pages.response import PageResponse, EnumJS

from core.app.system.changelog.service import ChangeLogCommandService, ChangeLogQueryService

from .request import ChangeLogRequest

router = APIRouter(prefix="/changelog")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_changelog_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/changelog/" + pathFile)


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_w())
async def page_system_changelog_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await ChangeLogQueryService().datatable_changelog(params=params)


@router.post("/{PathCheck}", status_code=201, dependencies=page.depend_w())
async def page_system_changelog_create(dataIn: ChangeLogRequest, req: page_req):
    data_get = await ChangeLogQueryService().get_changelog_by(version_name=dataIn.version_name)
    if data_get is not None:
        errors = [{"loc": ["body", "version_name"], "msg": "duplicate version_name is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    await ChangeLogCommandService().create_changelog(
        version_name=dataIn.version_name,
        dateupdate=datetime.today(),
        description=dataIn.description,
        created_user=req.user.username,
    )


@router.delete("/{PathCheck}/{changelog_id:int}", status_code=202, dependencies=page.depend_d())
async def page_system_changelog_delete(changelog_id: int, req: page_req):
    await ChangeLogQueryService().get_changelog(changelog_id)
    await ChangeLogCommandService().delete_changelog(changelog_id, req.user.username)
