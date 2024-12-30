from datetime import date

from pydantic import BaseModel, Field


class SysRepoSchema(BaseModel):
    id: int = Field(None, description="ID")
    name: date = Field(None, description="name")
    allocation: str = Field(None, description="allocation for")
    datalink: str = Field(None, description="datalink")
    user: str = Field(None, description="user at datalink")
    password: str = Field(None, description="pass at datalink")
    is_active: bool = Field(None, description="description")
