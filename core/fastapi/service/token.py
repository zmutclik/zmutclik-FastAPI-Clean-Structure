from typing import Union
from datetime import timedelta, datetime

from jose import JWTError, jwt
from core import config
from core.exceptions import InactiveUserScopeException


def token_create(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return encoded_jwt


# def user_access_token(db, userName, scopeAuth, scopeUser, timeout: int):
#     scopesPass = ["default"]
#     for item in scopeAuth:
#         if item not in scopeUser:
#             raise InactiveUserScopeException("Inactive user scope : " + item)
#         else:
#             scopesPass.append(item)
#     access_token = token_create(
#         data={"sub": userName, "scopes": scopesPass},
#         expires_delta=timedelta(minutes=timeout),
#     )
#     return access_token
