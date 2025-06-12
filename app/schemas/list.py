from pydantic import BaseModel
from typing import List as ListType, Optional

class ListBase(BaseModel):
    titulo: str
    posicao: int

class ListCreate(ListBase):
    board_id: int 


class ListUpdate(ListBase):
    titulo: Optional[str] = None


class ListDelete(BaseModel):
    id: int 


class ListOut(ListCreate):
    id: int
    titulo: str
    posicao: int
    board_id: int

    class Config:
        from_attributes = True

