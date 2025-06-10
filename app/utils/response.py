from fastapi.responses import JSONResponse
from typing import Any

def create_response(data: Any = None, message: str = "Success", code: int = 200, error: bool = False):
    return JSONResponse(
        status_code=code,
        content={
            "error": error,
            "message": message,
            "code": code,
            "data": data,
        }
    )
