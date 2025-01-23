import os
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Response, Depends
from core.config import config
from fastapi.responses import RedirectResponse
from core.pages.response import PageResponse

router = APIRouter(prefix="/logout", tags=["AUTH / OUT"])
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("/{username}", status_code=201, dependencies=page.dependencies())
def page_auth_logout(response: Response, request: page_req):
    response.delete_cookie(key=config.COOKIES_KEY)

    # SessionRepository().disable(req.state.sessionId)
    # thread = threading.Thread(target=SessionRepository().migrasi())
    # thread.start()

    sleep(1)
    response.status_code = 302  # Bisa diganti 301 atau 307 sesuai kebutuhan
    response.headers["Location"] = f"/auth/login"
    return response
