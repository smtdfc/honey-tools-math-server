from typing import Any, Optional
from pydantic import BaseModel
from sympy import Union

from schema.entites import MathJSON


class SimplifyRequestBody(BaseModel):
    expr: MathJSON


class DiffRequestBody(BaseModel):
    expr: MathJSON
    var: str
    order: int


class IntegrateRequestBody(BaseModel):
    expr: MathJSON
    var: str
    a: Optional[MathJSON]
    b: Optional[MathJSON]
