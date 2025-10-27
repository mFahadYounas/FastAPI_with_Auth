from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    status: int
    error_msg: str
    data: T
