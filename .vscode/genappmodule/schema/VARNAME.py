from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CLASSNAMESchema(BaseModel):
    id: int 
    VARNAME: str 
