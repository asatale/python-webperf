from pydantic import BaseModel


class ResponseModel(BaseModel):
    result: str
    message: str
