from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field 
 
 
class ClientSchema(BaseModel): 
    client_id: str 
    platform: str 
    browser: str 
