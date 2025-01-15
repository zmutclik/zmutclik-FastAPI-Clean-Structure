from datetime import datetime

from pydantic import BaseModel, Field


class PrivilegeMenuSchema(BaseModel):
    id: int
    privilege_id: int
    menu_id: int
