from typing import Any, Union
from pydantic import BaseModel


MathJSON = Union[list[Any], Any]


class SimplifyResult(BaseModel):
    input: str
    output: str
    error: str | None = None


class DiffResult(BaseModel):
    input: str
    var: str
    order: int
    output: str
    error: str | None = None


class IntegrateResult(BaseModel):
    input: str
    var: str
    a: MathJSON
    b: MathJSON
    output: str
    error: str | None = None
