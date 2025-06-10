import os
import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import create_response

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException: {exc.detail} | Status Code: {exc.status_code} | Path: {request.url.path}")
    return create_response(
        message=exc.detail,
        code=exc.status_code,
        error=True
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"ValidationError on {request.url.path}: {exc.errors()}")
    return create_response(
        message="Validation error",
        code=422,
        error=True,
        data=exc.errors()
    )
