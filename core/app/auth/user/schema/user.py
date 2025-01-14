from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .user_privilege import UserPrivilegeSchema
from .user_scope import UserScopeSchema


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    nohp: str
    full_name: str
    disabled: bool
    created_at: datetime
    updated_at: datetime

    # PRIVILEGE: Optional[list[UserPrivilegeSchema]]
    # SCOPE: Optional[list[UserScopeSchema]]

