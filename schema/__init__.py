from typing import Any, Generic, Literal, TypeVar
from pydantic import BaseModel


class SimplifyResult(BaseModel):
    input: str
    output: str
    error: str | None = None


T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    status: Literal["success", "error"]
    data: T | None = None
    error: str | None = None
