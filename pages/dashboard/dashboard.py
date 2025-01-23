import os
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse

router = APIRouter(prefix="/dashboard")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix, depend_roles=[])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_r())
async def page_dashboard(req: page_req):
    return page.response(req, "/html/index.html")
