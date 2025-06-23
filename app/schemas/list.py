from pydantic import BaseModel
from typing import List as ListResponse, Optional

from app.schemas.task import TaskOut

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
    tasks: ListResponse[TaskOut]

    class Config:
        from_attributes = True

