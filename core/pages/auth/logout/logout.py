import os
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Response, Depends
from core.config import config_auth
from core.pages.response import PageResponse
from core.app.security.session.service import SessionService

router = APIRouter(prefix="/logout", tags=["AUTH / OUT"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("/{username}", status_code=201, dependencies=page.dependencies())
async def page_auth_logout(response: Response, request: page_req, redirect_uri: str = None):
    response.delete_cookie(key=config_auth.COOKIES_KEY)
    response.delete_cookie(key=config_auth.REFRESH_KEY)

    await SessionService().deavtive_session(request.user.client_id)

    sleep(1)
    response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    if redirect_uri is None:
        redirect_uri = f"/auth/loggedin"
        
    response.headers["Location"] = redirect_uri
    return response
