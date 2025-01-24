from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, Field, field_validator


class LogErrorResponse(BaseModel):
    error_type: str
    error_message: str
    error_traceback: str
