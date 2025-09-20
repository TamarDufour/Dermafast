from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

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

class MoleAnalysisRequest(BaseModel):
    national_id: str
    image_base64: str

class SimilarMoleSelection(BaseModel):
    selected_ids: List[str] = Field(..., max_items=3)
