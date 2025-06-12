from pydantic import BaseModel
from typing import Optional, List


class BoardCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None


class BoardUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str]= None

class BoarDelete(BaseModel):
    id: int


class BoardOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True
