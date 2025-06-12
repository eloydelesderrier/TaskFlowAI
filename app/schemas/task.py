from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    posicao: int
    venci_data: Optional[datetime] = None
    prioridade: Optional[str] = None

class TaskCreate(TaskBase):
    list_id: int

class TaskUpdate(TaskBase):
    titulo: str
    descricao: Optional[str] = None
    posicao: int
    venci_data: Optional[datetime] = None
    prioridade: Optional[str] = None


class TaskDelete(TaskBase):
    id: int

class TaskMove(BaseModel):
    move_list_id: int
    nova_posicao: int

class TaskOut(TaskBase):
    id: int
    list_id: int

    class Config:
        from_attributes = True

