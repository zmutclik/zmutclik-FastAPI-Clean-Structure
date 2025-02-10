import os
import requests
import threading
from time import sleep
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.app.auth.user.service import UserQueryService, UserCommandService
from core.pages.auth.register.request import RegisterRequest
from fastapi.exceptions import RequestValidationError
from core import config
from core.pages.response import PageResponse
from core.utils import telegram_bot_sendtext

router = APIRouter(prefix="/register")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page.prefix_url = "/auth" + router.prefix
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_register(req: page_req):
    return page.response(req, "/html/register.html")


@router.get("/{PathCheck}/register.js")
async def page_js_register(req: page_req):
    return page.response(req, "/html/register.js")


@router.post("/{PathCheck}/register", status_code=201)
async def post_register(dataIn: RegisterRequest, req: page_req):
    sleep(1)
    if dataIn.password != dataIn.password2:
        errors = [{"loc": ["body", "password"], "msg": "password tidak sama", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    await UserQueryService().validate_user(dataIn.username, dataIn.email, dataIn.nohp)

    data_created = await UserCommandService().create_user(
        created_user="form_register",
        username=dataIn.username,
        email=dataIn.email,
        full_name=dataIn.full_name,
        nohp=dataIn.nohp,
        password1=dataIn.password,
        password2=dataIn.password2,
    )

    await telegram_bot_sendtext("register_alert", {"app": config.APP_NAME, "user": data_created.username, "email": data_created.email})
