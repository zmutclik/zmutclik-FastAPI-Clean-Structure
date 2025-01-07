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
    def __init__(self):
        # self.logs_repo = LogsRepo()
        pass

    async def start(self, request: Request):
        if request.user.channel == "page":
            if request.user.client_id == None:
                request.user.client_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
            if request.user.session_id == None:
                request.user.session_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))

        self.data_created = Logs.create(request=request)

        return request

    def finish(self, request: Request, response: Response):
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

        if self.data_created.channel == "page":
            response.set_cookie(key=config.CLIENT_KEY, value=request.user.client_id)

        if request.user.channel != "page_js" or request.user.channel != "static":
            threading.Thread(target=LogsRepo().save(self.data_created)).start()
