from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class AuthConfigSchema(BaseModel): 
    jwt_scret_key: str
    jwt_algorithm: str 
    cookies_prefix: str 
    cookies_https: bool 
    cookies_exp: int 
    refresh_exp: int 
    