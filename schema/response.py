from typing import Generic, Literal, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: str | None = None
    status: Literal["success", "error"]

    model_config = {"arbitrary_types_allowed": True}
