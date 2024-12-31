import random
import string
import time
import threading
import asyncio
from typing import Union
from pythondi import inject

from fastapi import Request, Response

from app._sys.logs.domain import Logs
from app._sys.logs.repository import LogsRepo
from app._sys.logs.schema import LogsSchema

from core import config

# from app._sys.logs.exceptions import LogsNotFoundException, LogsDuplicateException


class LogsService:
    @inject()
    def __init__(self, logs_repo: LogsRepo):
        self.logs_repo = logs_repo

    def generateId(self, request: Request, key: str):
        id_ = request.cookies.get(key)
        if id_ is None:
            id_ = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        return id_

    def getIp(self, request: Request):
        ipaddress = request.client.host
        ipproxy = ""
        try:
            if request.headers.get("X-Real-IP") is not None:
                ipaddress = request.headers.get("X-Real-IP")
                ipproxy = request.client.host
        except:
            pass
        return ipaddress, ipproxy

    async def create_logs(self, request: Request):
        routername = request.scope["route"].name
        channel = ""
        clientId = ""
        if "api" in routername:
            channel = "api"
        if "page" in routername:
            channel = "page"
            clientId = self.generateId(request, config.CLIENT_KEY)

        request.state.islogsave = True
        request.state.clientId = clientId
        request.state.appchannel = channel

        self.data_created = Logs.create(request=request)

        return request

    async def finish(self, request: Request, response: Response):
        self.data_created.user = request.user.username
        self.data_created.status_code = response.status_code
        self.data_created.process_time = time.time() - self.data_created.startTime
        if self.data_created.channel == "page":
            response.set_cookie(key=config.CLIENT_KEY, value=self.data_created.client_id)

        if request.state.islogsave and "/static/" not in self.data_created.path:
            asyncio.create_task(self.logs_repo.save(logs=self.data_created))
