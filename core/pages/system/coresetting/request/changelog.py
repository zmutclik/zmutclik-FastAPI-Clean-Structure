from datetime import date

from pydantic import BaseModel, Field


class ChangeLogRequest(BaseModel):
    version_name: str
    description: str
