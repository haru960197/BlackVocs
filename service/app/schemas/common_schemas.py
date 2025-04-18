# common_schemas.py

from pydantic import BaseModel

class SuccessMsg(BaseModel):
    message: str

class ErrorMsg(BaseModel):
    message: str
