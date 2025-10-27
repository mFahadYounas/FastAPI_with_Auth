from typing import Generic, TypeVar
from app.schemas.api_response import APIResponse
from fastapi import HTTPException

T = TypeVar("T")


class ResponseBuilder(Generic[T]):
    @staticmethod
    def success(data: T):
        return APIResponse[T](status=200, error_msg="", data=data)

    @staticmethod
    def error(status: int, error_msg: str):
        raise HTTPException(status_code=status, detail=error_msg)
