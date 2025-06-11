from fastapi import APIRouter, FastAPI
from app.utils.response import create_response
from app.utils.exception_handlers import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.auth import routes as auth_routes
from app.products import public_routes as public_routes
from app.products import admin_routes as admin_routes
from app.cart import routes as cart_routes
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

router = APIRouter(tags=["Root"])
@app.get("/")
async def health_check():
    return create_response(data={"message": "Health Check is done."})

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)    

app.include_router(auth_routes.router)
app.include_router(public_routes.router)
app.include_router(admin_routes.router)
app.include_router(cart_routes.router) 