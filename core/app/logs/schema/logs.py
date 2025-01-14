from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field


class LogsSchema(BaseModel):
    id: int = Field(None, description="ID")
    startTime: time = Field(None, description="start time")
    app: str = Field(None, description="application name")
    channel: str = Field(None, description="application channel")
    platform: str = Field(None, description="platform client")
    browser: str = Field(None, description="browser client")
    referer: str = Field(None, description="referer link")
    router: str = Field(None, description="router name")
    path: str = Field(None, description="path url")
    method: str = Field(None, description="method url")
    ipaddress: str = Field(None, description="ipaddress client")
    ipproxy: str = Field(None, description="ipaddress proxy")
    username: str = Field(None, description="user access")
    status_code: int = Field(None, description="status_code response")
    process_time: float = Field(None, description="duration process_time")
