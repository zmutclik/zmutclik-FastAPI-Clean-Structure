import random
import string
import time
import asyncio

from fastapi import Request, Response

from core.app.logs.domain import Logs
from core.app.logs.repository import LogsRepo
from core.app.logs.schema import LogsSchema, LogErrorSchema
from core.app.security.client.service import ClientService

from core import config_auth


class LogsService:
    def __init__(self):
        self.new_client_id = False
        pass

    async def start(self, request: Request):
        if request.user.channel == "page":
            if request.user.client_id == None:
                request.user.client_id = await ClientService().new_client(request)
                self.new_client_id = True
            if request.user.session_id == None:
                request.user.session_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))

        self.data_created = Logs.create(request=request)

        return request

    def finish(self, request: Request, response: Response, traceerror: LogErrorSchema):
        try:
            routername = request.scope["route"].name
        except:
            if "static" in request.scope["path"]:
                routername = "static"
            else:
                routername = ""
        self.data_created.router = routername
        self.data_created.user = request.user.username
        self.data_created.status_code = response.status_code
        self.data_created.process_time = time.time() - self.data_created.startTime

        if self.data_created.channel == "page" and self.new_client_id:
            response.set_cookie(key=config_auth.CLIENT_KEY, value=request.user.client_id, httponly=True)

        # if request.user.channel != "page_js" or request.user.channel != "static":
        asyncio.create_task(LogsRepo().save(self.data_created, traceerror))
