from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import create_response

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return create_response(message=exc.detail, code=exc.status_code, error=True)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_response(
        message="Validation error",
        code=422,
        error=True,
        data=exc.errors()
    )
