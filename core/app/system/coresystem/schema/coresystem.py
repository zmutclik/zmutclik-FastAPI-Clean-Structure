from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CoreSYSTEMSchema(BaseModel):
    environment: str
    app_name: str
    app_desc: str
    app_host: str
    app_port: int
    jwt_scret_key: str
    jwt_algorithm: str
    prefix_session: str
    cookies_exp: int
    refresh_exp: int
    debug: bool
