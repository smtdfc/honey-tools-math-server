from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import ResponseModel, SimplifyResult
import core

origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/simplify", response_model=ResponseModel[SimplifyResult])
def simplify(expr: str) -> ResponseModel[SimplifyResult]:
    result = core.simplify(expr)

    if result.error:
        raise HTTPException(
            status_code=400,
            detail=ResponseModel[SimplifyResult](
                status="error", error=result.error
            ).model_dump(),
        )

    return ResponseModel[SimplifyResult](status="success", data=result)
