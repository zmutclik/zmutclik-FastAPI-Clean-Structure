import os
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Response, Depends
from core.config import config_auth
from core.exceptions import RequiresLoginException
from core.pages.response import PageResponse
from ..logout.logout import page_auth_logout

router = APIRouter(prefix="/timeout", tags=["AUTH / OUT"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("/{username}", status_code=201)
async def page_auth_timeout(response: Response, request: page_req):
    return await page_auth_logout(response, request)
