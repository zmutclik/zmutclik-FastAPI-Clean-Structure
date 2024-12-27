from datetime import datetime

from pydantic import BaseModel, Field


class PrivilegeSchema(BaseModel):
    id: int = Field(None, description="ID")
    privilege: str = Field(None, description="Privilege name")
    desc: str = Field(None, description="description")
