from datetime import datetime

from pydantic import BaseModel

class GetUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    nohp: str
    disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "hide",
                "email": "hide@hide.com",
                "nohp": "0810000001",
                "full_name": "Some Person",
                "disabled": False,
                "created_at": "2021-11-11T07:50:54.289Z",
                "updated_at": "2021-11-11T07:50:54.289Z",
            }
        }