from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .user_privilege import UserPrivilegeSchema
from .user_scope import UserScopeSchema


class UserSchema(BaseModel):
    id: int = Field(None, description="ID")
    username: str = Field(None, description="Username")
    email: str = Field(None, description="Email")
    nohp: str = Field(None, description="No HP")
    full_name: str = Field(None, description="Full Name")
    disabled: bool = Field(None, description="Is Disabled")
    created_at: datetime = Field(None, description="Create Time")
    updated_at: datetime = Field(None, description="Update Time")

    # PRIVILEGE: Optional[list[UserPrivilegeSchema]]
    # SCOPE: Optional[list[UserScopeSchema]]
