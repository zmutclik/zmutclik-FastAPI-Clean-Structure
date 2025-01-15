from datetime import datetime

from pydantic import BaseModel, Field


class PrivilegeSchema(BaseModel):
    id: int 
    privilege: str 
    desc: str 
