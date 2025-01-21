from datetime import date

from pydantic import BaseModel, Field


class SysRepoRequest(BaseModel):
    name: str
    allocation: str
    datalink: str
    user: str
    password: str
    is_active: bool
