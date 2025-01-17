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

router = APIRouter(prefix="/register")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url=router.prefix)
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse)
async def page_register(req: page_req):
    print("page[login]requser ", req.user)
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

    data_filter = await UserQueryService().get_user_by(username=dataIn.username)
    if data_filter is not None:
        errors = [{"loc": ["body", "username"], "msg": "duplicate username is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_filter = await UserQueryService().get_user_by(email=dataIn.email)
    if data_filter is not None:
        errors = [{"loc": ["body", "email"], "msg": "duplicate email is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_filter = await UserQueryService().get_user_by(nohp=dataIn.nohp)
    if data_filter is not None:
        errors = [{"loc": ["body", "nohp"], "msg": "duplicate nohp is use", "type": "value_error.duplicate"}]
        raise RequestValidationError(errors)

    data_created = await UserCommandService().create_user(
        created_user="form_register",
        username=dataIn.username,
        email=dataIn.email,
        full_name=dataIn.full_name,
        nohp=dataIn.nohp,
        password1=dataIn.password,
        password2=dataIn.password2,
    )

    thread = threading.Thread(target=telegram_bot_sendtext, args=(data_created.username, data_created.email, data_created.id))
    thread.start()


def telegram_bot_sendtext(username, email, id):
    message = """<b>AKUN SUKSES TERDAFTAR</b>
<code>app   : {}</code>
<code>user  : {}</code>
<code>email : {}</code>
    """
    message = message.format(config.APP_NAME, username, email, id)
    rtoken = requests.get("https://pastebin.com/raw/EekQSJGY")
    bot_token = rtoken.content.decode()
    bot_chatID = "28186920"
    url_param_1 = "sendMessage"
    url_param_2 = ""
    url_param_3 = ""
    send_url = "https://api.telegram.org/bot{}/{}?chat_id={}&parse_mode=html{}&text={}{}"
    send_text = send_url.format(bot_token, url_param_1, bot_chatID, url_param_2, message, url_param_3)
    response = requests.get(send_text)
    return response.json()
