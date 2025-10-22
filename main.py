from fastapi import FastAPI, HTTPException
from typing import Any, List
from fastapi.middleware.cors import CORSMiddleware
import core
from schema import DiffRequestBody, SimplifyRequestBody, BaseResponse
from schema.request import IntegrateRequestBody

origins = ["http://localhost:3000", "https://honey-tools.vercel.app"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/simplify", response_model=BaseResponse)
def simplify(body: SimplifyRequestBody) -> BaseResponse:
    result = core.simplify(body.expr)

    if result.error:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "error": result.error},
        )

    return BaseResponse(status="success", data=result)


@app.post("/api/v1/diff", response_model=BaseResponse)
def diff(body: DiffRequestBody) -> BaseResponse:
    result = core.derivative(body.expr, body.var, body.order)

    if result.error:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "error": result.error},
        )

    return BaseResponse(status="success", data=result)


@app.post("/api/v1/integrate", response_model=BaseResponse)
def integrate(body: IntegrateRequestBody) -> BaseResponse:
    result = core.integrate_expr(body.expr, body.var, body.a, body.b)

    if result.error:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "error": result.error},
        )

    return BaseResponse(status="success", data=result)
