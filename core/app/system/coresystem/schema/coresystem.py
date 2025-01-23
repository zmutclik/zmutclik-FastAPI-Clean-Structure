from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CoreSYSTEMSchema(BaseModel):
    environment: str
    app_name: str
    app_desc: str
    app_host: str
    app_port: int
    client_key: str
    jwt_scret_key: str
    jwt_algorithm: str
    cookies_key: str
    cookies_exp: int
    debug: bool
