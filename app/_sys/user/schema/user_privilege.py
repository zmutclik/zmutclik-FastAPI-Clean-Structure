from datetime import datetime

from pydantic import BaseModel, Field


class UserPrivilegeSchema(BaseModel):
    privilege: str = Field(None, description="Privilege name")
    desc: str = Field(None, description="description")
