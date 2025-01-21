from datetime import date

from pydantic import BaseModel, Field


class SysRepoResponse(BaseModel):
    id: int
    name: str
    allocation: str
    datalink: str
    user: str
    password: str
    is_active: bool
