from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    national_id: str
    password: str

class UserLogin(BaseModel):
    national_id: str
    password: str

class UserResponse(BaseModel):
    national_id: str
    message: str
    last_login: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    national_id: str
    last_login: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
