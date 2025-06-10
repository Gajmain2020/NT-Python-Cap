from pydantic import BaseModel, EmailStr, constr
from typing import Literal

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)
    role: Literal['admin', 'user']

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordSchema(BaseModel):
    new_password: str

class ForgotPasswordRequestSchema(BaseModel):
    email: EmailStr