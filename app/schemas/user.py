from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime

    class config:
        from_attributes = True

class UserUpdate(BaseModel):
    senha: Optional[str] = None

class UserDelete(BaseModel):
    id: int

class TokenBlacklistCreate(BaseModel):
    jti: str

class TokenBlacklistOut(BaseModel):
    id: int
    jti: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr

