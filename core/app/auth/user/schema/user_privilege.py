from datetime import datetime

from pydantic import BaseModel, Field


class UserPrivilegeSchema(BaseModel):
    id: int
    privilege: str
    desc: str
