from datetime import date

from pydantic import BaseModel, Field


class ChangeLogSchema(BaseModel):
    id: int = Field(None, description="ID")
    dateupdate: date = Field(None, description="date updated")
    version_name: str = Field(None, description="version name")
    description: str = Field(None, description="description")
