from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field


class LogsSchema(BaseModel):
    id: int
    startTime: time
    app: str
    channel: str
    platform: str
    browser: str
    referer: str
    router: str
    path: str
    method: str
    ipaddress: str
    ipproxy: str
    username: str
    status_code: int
    process_time: float


